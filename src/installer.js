import { homedir } from 'os';
import { join, dirname } from 'path';
import { existsSync, mkdirSync, cpSync, readFileSync, rmSync } from 'fs';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import ora from 'ora';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * Compare two semantic version strings
 * Returns: 1 if v1 > v2, -1 if v1 < v2, 0 if equal
 */
function compareVersions(v1, v2) {
  const parts1 = v1.split('.').map(Number);
  const parts2 = v2.split('.').map(Number);

  for (let i = 0; i < 3; i++) {
    if (parts1[i] > parts2[i]) return 1;
    if (parts1[i] < parts2[i]) return -1;
  }
  return 0;
}

/**
 * Extract version from SKILL.md frontmatter or return null
 */
function getInstalledVersion(skillDir) {
  const skillMdPath = join(skillDir, 'SKILL.md');
  if (!existsSync(skillMdPath)) return null;

  try {
    const content = readFileSync(skillMdPath, 'utf-8');
    const versionMatch = content.match(/^version:\s*(.+)$/m);
    if (versionMatch) return versionMatch[1].trim();
  } catch (error) {
    // Ignore errors, treat as no version found
  }
  return null;
}

export async function installSkill(skill, options = {}) {
  const { force = false } = options;
  const spinner = ora(`Installing ${chalk.cyan(skill.name)}`).start();

  try {
    // Determine target directory
    const targetDir = join(process.cwd(), '.claude', 'skills', skill.name);

    // Check if skill already exists
    if (existsSync(targetDir)) {
      const installedVersion = getInstalledVersion(targetDir);
      const newVersion = skill.version;

      if (!installedVersion) {
        // No version info in installed skill
        if (force) {
          spinner.info(chalk.yellow(`Reinstalling ${skill.name}...`));
          rmSync(targetDir, { recursive: true, force: true });
        } else {
          spinner.warn(chalk.yellow(`${skill.name} already exists (unknown version), skipping. Use --force to reinstall`));
          return { skipped: true, reason: 'exists-no-version' };
        }
      } else if (compareVersions(newVersion, installedVersion) > 0) {
        // Newer version available
        spinner.info(chalk.blue(`Updating ${skill.name}: ${installedVersion} → ${newVersion}`));
        rmSync(targetDir, { recursive: true, force: true });
      } else if (compareVersions(newVersion, installedVersion) === 0) {
        // Same version
        if (force) {
          spinner.info(chalk.yellow(`Reinstalling ${skill.name} v${newVersion}...`));
          rmSync(targetDir, { recursive: true, force: true });
        } else {
          spinner.succeed(chalk.green(`${skill.name} v${installedVersion} is already up to date`));
          return { skipped: true, reason: 'up-to-date' };
        }
      } else {
        // Installed version is newer (downgrade)
        spinner.warn(chalk.yellow(`${skill.name} v${installedVersion} is newer than available v${newVersion}, skipping`));
        return { skipped: true, reason: 'newer-installed' };
      }
    }

    // Create .claude/skills directory if it doesn't exist
    const skillsDir = join(process.cwd(), '.claude', 'skills');
    if (!existsSync(skillsDir)) {
      mkdirSync(skillsDir, { recursive: true });
    }

    // Source directory (where the skill files are in the package)
    const sourceDir = join(__dirname, '..', 'skills', skill.name);

    if (!existsSync(sourceDir)) {
      spinner.fail(chalk.red(`Skill source not found: ${skill.name}`));
      return { success: false, error: 'source-not-found' };
    }

    // Copy skill files
    cpSync(sourceDir, targetDir, { recursive: true });

    spinner.succeed(chalk.green(`Installed ${chalk.bold(skill.name)} v${skill.version}`));
    return { success: true, version: skill.version };
  } catch (error) {
    spinner.fail(chalk.red(`Failed to install ${skill.name}: ${error.message}`));
    return { success: false, error: error.message };
  }
}

// Utility to get Claude config directory
export function getClaudeConfigDir() {
  const home = homedir();
  return join(home, '.claude');
}

// Check if running in a project directory (has .claude folder or can create one)
export function isValidProjectDirectory() {
  const claudeDir = join(process.cwd(), '.claude');
  return existsSync(claudeDir) || true; // Allow creating .claude directory
}

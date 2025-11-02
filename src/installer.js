import { homedir } from 'os';
import { join, dirname } from 'path';
import { existsSync, mkdirSync, cpSync } from 'fs';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import ora from 'ora';

const __dirname = dirname(fileURLToPath(import.meta.url));

export async function installSkill(skill) {
  const spinner = ora(`Installing ${chalk.cyan(skill.name)}`).start();

  try {
    // Determine target directory
    const targetDir = join(process.cwd(), '.claude', 'skills', skill.name);

    // Check if skill already exists
    if (existsSync(targetDir)) {
      spinner.warn(chalk.yellow(`${skill.name} already exists, skipping`));
      return;
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
      return;
    }

    // Copy skill files
    cpSync(sourceDir, targetDir, { recursive: true });

    spinner.succeed(chalk.green(`Installed ${chalk.bold(skill.name)}`));
  } catch (error) {
    spinner.fail(chalk.red(`Failed to install ${skill.name}: ${error.message}`));
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

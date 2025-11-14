import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import { showInteractiveMenu } from './interactive.js';
import { installSkill } from './installer.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

export async function run() {
  const args = process.argv.slice(2);

  // Load marketplace data
  const marketplacePath = join(__dirname, '..', '.claude-plugin', 'marketplace.json');
  const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf-8'));

  // Display header
  console.log('\n' + chalk.bold.cyan('┌─────────────────────────────────────────┐'));
  console.log(chalk.bold.cyan('│  Claude Code Skills by Giorris          │'));
  console.log(chalk.bold.cyan('└─────────────────────────────────────────┘') + '\n');
  console.log(chalk.gray(`📦 ${marketplace.plugins.length} skills available\n`));

  // Parse flags
  const force = args.includes('--force') || args.includes('-f');
  const filteredArgs = args.filter(a => a !== '--force' && a !== '-f');

  // Parse command
  if (filteredArgs.length === 0) {
    // Interactive mode
    await showInteractiveMenu(marketplace);
  } else if (filteredArgs[0] === 'install' && filteredArgs[1]) {
    // Direct install: npx @giorris/claude-skills install ai-component-metadata
    const skillName = filteredArgs[1];
    const skill = marketplace.plugins.find(p => p.name === skillName);

    if (!skill) {
      console.error(chalk.red(`✗ Skill "${skillName}" not found`));
      console.log(chalk.gray('\nAvailable skills:'));
      marketplace.plugins.forEach(s => {
        console.log(chalk.cyan(`  • ${s.name}`));
      });
      process.exit(1);
    }

    await installSkill(skill, { force });
  } else if (filteredArgs[0] === '--all') {
    // Install all skills
    console.log(chalk.yellow('Installing all skills...\n'));
    for (const skill of marketplace.plugins) {
      await installSkill(skill, { force });
    }
    console.log(chalk.green('\n✓ All skills processed!'));
  } else if (filteredArgs[0] === '--help' || filteredArgs[0] === '-h') {
    showHelp();
  } else {
    console.error(chalk.red('✗ Unknown command'));
    showHelp();
    process.exit(1);
  }
}

function showHelp() {
  console.log(chalk.bold('\nUsage:'));
  console.log('  npx giorris-claude-skills                     ' + chalk.gray('# Interactive mode'));
  console.log('  npx giorris-claude-skills install <name>      ' + chalk.gray('# Install specific skill'));
  console.log('  npx giorris-claude-skills install <name> --force ' + chalk.gray('# Force reinstall'));
  console.log('  npx giorris-claude-skills --all               ' + chalk.gray('# Install all skills'));
  console.log('  npx giorris-claude-skills --help              ' + chalk.gray('# Show this help'));
  console.log(chalk.bold('\nOptions:'));
  console.log('  --force, -f  ' + chalk.gray('Force reinstall even if already installed'));
  console.log(chalk.bold('\nExamples:'));
  console.log('  npx giorris-claude-skills install ai-component-metadata');
  console.log('  npx giorris-claude-skills install codebase-index --force');
  console.log('  npx giorris-claude-skills --all\n');
}

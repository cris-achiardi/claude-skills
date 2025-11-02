import inquirer from 'inquirer';
import chalk from 'chalk';
import { installSkill } from './installer.js';

export async function showInteractiveMenu(marketplace) {
  // Create choices from marketplace plugins
  const choices = marketplace.plugins.map(skill => ({
    name: `${chalk.bold(skill.name)} ${chalk.gray(`(${skill.category})`)} - ${skill.description}`,
    value: skill.name,
    short: skill.name
  }));

  choices.push(new inquirer.Separator());
  choices.push({
    name: chalk.yellow('Install all skills'),
    value: '__all__'
  });

  // Show skill selection
  const { selectedSkills } = await inquirer.prompt([
    {
      type: 'checkbox',
      name: 'selectedSkills',
      message: 'Select skills to install:',
      choices,
      pageSize: 10,
      validate: (answer) => {
        if (answer.length === 0) {
          return 'You must select at least one skill';
        }
        return true;
      }
    }
  ]);

  // Handle "install all" option
  let skillsToInstall = [];
  if (selectedSkills.includes('__all__')) {
    skillsToInstall = marketplace.plugins;
  } else {
    skillsToInstall = marketplace.plugins.filter(s => selectedSkills.includes(s.name));
  }

  // Confirm installation
  console.log(chalk.bold('\nSkills to install:'));
  skillsToInstall.forEach(skill => {
    console.log(chalk.cyan(`  ✓ ${skill.name}`));
  });

  const { confirm } = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'confirm',
      message: 'Proceed with installation?',
      default: true
    }
  ]);

  if (!confirm) {
    console.log(chalk.yellow('\nInstallation cancelled'));
    return;
  }

  // Install skills
  console.log('');
  for (const skill of skillsToInstall) {
    await installSkill(skill);
  }

  console.log(chalk.green.bold('\n✓ Installation complete!'));
  console.log(chalk.gray('\nYour skills are now available in Claude Code.'));
  console.log(chalk.gray('No restart required - skills are active immediately.\n'));
}

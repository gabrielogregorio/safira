import * as Menubar from '@radix-ui/react-menubar';
import type { ReactNode } from 'react';
import { examples } from '@/content/content';
import { useTranslation } from '@/i18n/i18n';
import type { RunMode } from '@/runtime/protocol';
import type { Settings, ThemeId } from '@/settings/settings';
import { clampFontSize } from '@/settings/settings';

interface IdeMenuBarProps {
  settings: Settings;
  isRunning: boolean;
  onOpenFile: () => void;
  onNewTab: () => void;
  onSave: () => void;
  onSaveAs: () => void;
  onFormat: () => void;
  onExportProject: () => void;
  onImportArchive: () => void;
  onRun: (mode: RunMode) => void;
  onStop: () => void;
  onToggleBreakpoint: () => void;
  onClearBreakpoints: () => void;
  onOpenExample: (id: string, text: string) => void;
  onChangeSettings: (changes: Partial<Settings>) => void;
  onToggleFullScreen: () => void;
  onShowCommands: () => void;
}

interface MenuProps {
  label: string;
  children: ReactNode;
}

interface ActionProps {
  label: string;
  shortcut?: string;
  disabled?: boolean;
  onSelect: () => void;
}

interface ThemeSubmenuProps {
  label: string;
  value: ThemeId;
  onChange: (theme: ThemeId) => void;
}

const BUG_REPORT_URL = 'https://github.com/safira-lang/safira-ide/issues';
const BLOG_URL = 'https://safiralang.blogspot.com/';
const THEME_IDS: ThemeId[] = ['light', 'dark', 'simple'];
const FONT_STEP = 1;
const PROGRAM_PREFIX = 'programa-';
const SUBMENU_OFFSET = 4;
const MENU_OFFSET = 6;

const Menu = ({ label, children }: MenuProps) => (
  <Menubar.Menu>
    <Menubar.Trigger className="menubar-trigger">{label}</Menubar.Trigger>
    <Menubar.Portal>
      <Menubar.Content className="menubar-content" align="start" sideOffset={MENU_OFFSET} collisionPadding={8}>
        {children}
      </Menubar.Content>
    </Menubar.Portal>
  </Menubar.Menu>
);

const Action = ({ label, shortcut, disabled = false, onSelect }: ActionProps) => (
  <Menubar.Item className="menubar-item" disabled={disabled} onSelect={onSelect}>
    {label}
    {shortcut === undefined ? null : <span className="menubar-shortcut">{shortcut}</span>}
  </Menubar.Item>
);

const ThemeSubmenu = ({ label, value, onChange }: ThemeSubmenuProps) => {
  const t = useTranslation();
  const labels: Record<ThemeId, string> = { light: t('Light'), dark: t('Dark'), simple: t('Simple') };

  return (
    <Menubar.Sub>
      <Menubar.SubTrigger className="menubar-item">
        {label}
        <span className="menubar-shortcut" aria-hidden="true">
          ›
        </span>
      </Menubar.SubTrigger>
      <Menubar.Portal>
        <Menubar.SubContent className="menubar-content" sideOffset={SUBMENU_OFFSET} collisionPadding={8}>
          <Menubar.RadioGroup
            value={value}
            onValueChange={(theme) => {
              onChange(theme as ThemeId);
            }}>
            {THEME_IDS.map((theme) => (
              <Menubar.RadioItem key={theme} className="menubar-item menubar-radio" value={theme}>
                <Menubar.ItemIndicator className="menubar-indicator">●</Menubar.ItemIndicator>
                {labels[theme]}
              </Menubar.RadioItem>
            ))}
          </Menubar.RadioGroup>
        </Menubar.SubContent>
      </Menubar.Portal>
    </Menubar.Sub>
  );
};

export const IdeMenuBar = ({
  settings,
  isRunning,
  onOpenFile,
  onNewTab,
  onSave,
  onSaveAs,
  onFormat,
  onExportProject,
  onImportArchive,
  onRun,
  onStop,
  onToggleBreakpoint,
  onClearBreakpoints,
  onOpenExample,
  onChangeSettings,
  onToggleFullScreen,
  onShowCommands,
}: IdeMenuBarProps) => {
  const t = useTranslation();
  const lessons = examples.filter((example) => !example.id.startsWith(PROGRAM_PREFIX));
  const programs = examples.filter((example) => example.id.startsWith(PROGRAM_PREFIX));

  return (
    <Menubar.Root className="menubar" aria-label={t('Safira IDE')}>
      <Menu label={t('File')}>
        <Action label={t('Open file')} shortcut="Ctrl+O" onSelect={onOpenFile} />
        <Action label={t('New tab')} shortcut="Ctrl+N" onSelect={onNewTab} />
        <Menubar.Separator className="menubar-separator" />
        <Action label={t('Save')} shortcut="Ctrl+S" onSelect={onSave} />
        <Action label={t('Save as')} shortcut="Ctrl+Shift+S" onSelect={onSaveAs} />
        <Menubar.Separator className="menubar-separator" />
        <Action label={t('Export project (.zip)')} onSelect={onExportProject} />
        <Action label={t('Import .zip into this project')} onSelect={onImportArchive} />
        <Menubar.Separator className="menubar-separator" />
        <Action label={t('Format code')} onSelect={onFormat} />
      </Menu>
      <Menu label={t('Run')}>
        <Action
          label={t('Run all')}
          shortcut="Ctrl+Enter"
          onSelect={() => {
            onRun('run');
          }}
        />
        <Action
          label={t('Run line by line')}
          shortcut="F6"
          onSelect={() => {
            onRun('step');
          }}
        />
        <Action
          label={t('Run to breakpoint')}
          shortcut="F7"
          onSelect={() => {
            onRun('debug');
          }}
        />
        <Action label={t('Stop execution')} disabled={!isRunning} onSelect={onStop} />
        <Menubar.Separator className="menubar-separator" />
        <Action label={t('Toggle breakpoint')} shortcut="F10" onSelect={onToggleBreakpoint} />
        <Action label={t('Clear breakpoints')} onSelect={onClearBreakpoints} />
      </Menu>
      <Menu label={t('Examples')}>
        <Menubar.Label className="menubar-label">{t('Learn')}</Menubar.Label>
        {lessons.map((example) => (
          <Action
            key={example.id}
            label={example.title}
            onSelect={() => {
              onOpenExample(example.id, example.text);
            }}
          />
        ))}
        <Menubar.Separator className="menubar-separator" />
        <Menubar.Label className="menubar-label">{t('Programs')}</Menubar.Label>
        {programs.map((example) => (
          <Action
            key={example.id}
            label={example.title}
            onSelect={() => {
              onOpenExample(example.id, example.text);
            }}
          />
        ))}
      </Menu>
      <Menu label={t('Interface')}>
        <ThemeSubmenu
          label={t('Theme')}
          value={settings.theme}
          onChange={(theme) => {
            onChangeSettings({ theme });
          }}
        />
        <ThemeSubmenu
          label={t('Syntax colors')}
          value={settings.syntax}
          onChange={(syntax) => {
            onChangeSettings({ syntax });
          }}
        />
        <Menubar.Separator className="menubar-separator" />
        <Action
          label={t('Increase font')}
          onSelect={() => {
            onChangeSettings({ fontSize: clampFontSize(settings.fontSize + FONT_STEP) });
          }}
        />
        <Action
          label={t('Decrease font')}
          onSelect={() => {
            onChangeSettings({ fontSize: clampFontSize(settings.fontSize - FONT_STEP) });
          }}
        />
        <Action label={t('Full screen')} shortcut="F11" onSelect={onToggleFullScreen} />
      </Menu>
      <Menu label={t('Help')}>
        <Action label={t('Available commands')} onSelect={onShowCommands} />
        <Action
          label={t('Report a bug')}
          onSelect={() => {
            window.open(BUG_REPORT_URL, '_blank', 'noopener');
          }}
        />
        <Action
          label={t('Community blog')}
          onSelect={() => {
            window.open(BLOG_URL, '_blank', 'noopener');
          }}
        />
      </Menu>
    </Menubar.Root>
  );
};

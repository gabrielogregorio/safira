import * as Menubar from '@radix-ui/react-menubar';
import type { ReactNode } from 'react';
import { examples } from '@/content/content';
import { LOCALES, useTranslation } from '@/i18n/i18n';
import type { Locale } from '@/language/messages';
import type { RunMode } from '@/runtime/protocol';
import type { CodeFont, Settings } from '@/settings/settings';
import { clampFontSize, THEME_IDS } from '@/settings/settings';
import type { SoundName } from '@/ui/sound/sounds';

interface IdeMenuBarProps {
  settings: Settings;
  locale: Locale;
  isRunning: boolean;
  onNewTab: () => void;
  onSaveSnapshot: () => void;
  onShowHistory: () => void;
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
  onOpenLessons: () => void;
}

interface MenuProps {
  label: string;
  children: ReactNode;
}

interface ActionProps {
  label: string;
  shortcut?: string;
  disabled?: boolean;
  sound?: SoundName;
  onSelect: () => void;
}

interface RadioSubmenuProps<Value extends string> {
  label: string;
  value: Value;
  options: { id: Value; label: string }[];
  onChange: (value: Value) => void;
}

const BUG_REPORT_URL = 'https://github.com/safira-lang/safira-ide/issues';
const BLOG_URL = 'https://safiralang.blogspot.com/';
const FONT_STEP = 1;
const CODE_FONTS: { id: CodeFont; label: string }[] = [
  { id: 'mono', label: 'JetBrains Mono' },
  { id: 'aero', label: 'Istok Web' },
];
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

const Action = ({ label, shortcut, disabled = false, sound, onSelect }: ActionProps) => (
  <Menubar.Item className="menubar-item" disabled={disabled} data-sound={sound} onSelect={onSelect}>
    {label}
    {shortcut === undefined ? null : <span className="menubar-shortcut">{shortcut}</span>}
  </Menubar.Item>
);

const RadioSubmenu = <Value extends string>({ label, value, options, onChange }: RadioSubmenuProps<Value>) => (
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
          onValueChange={(next) => {
            onChange(next as Value);
          }}>
          {options.map((option) => (
            <Menubar.RadioItem key={option.id} className="menubar-item menubar-radio" value={option.id}>
              <Menubar.ItemIndicator className="menubar-indicator">●</Menubar.ItemIndicator>
              {option.label}
            </Menubar.RadioItem>
          ))}
        </Menubar.RadioGroup>
      </Menubar.SubContent>
    </Menubar.Portal>
  </Menubar.Sub>
);

export const IdeMenuBar = ({
  settings,
  locale,
  isRunning,
  onNewTab,
  onSaveSnapshot,
  onShowHistory,
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
  onOpenLessons,
}: IdeMenuBarProps) => {
  const t = useTranslation();
  const lessons = examples.filter((example) => !example.id.startsWith(PROGRAM_PREFIX));
  const programs = examples.filter((example) => example.id.startsWith(PROGRAM_PREFIX));
  const themeOptions = THEME_IDS.map((id) => ({
    id,
    label: { light: t('Light'), dark: t('Dark'), simple: t('Simple') }[id],
  }));

  return (
    <Menubar.Root className="menubar" aria-label={t('Safira IDE')}>
      <Menu label={t('File')}>
        <Action label={t('New tab')} shortcut="Ctrl+N" onSelect={onNewTab} />
        <Menubar.Separator className="menubar-separator" />
        <Action label={t('Save snapshot')} shortcut="Ctrl+S" sound="snapshot" onSelect={onSaveSnapshot} />
        <Action label={t('History')} onSelect={onShowHistory} />
        <Menubar.Separator className="menubar-separator" />
        <Action label={t('Export project (.zip)')} sound="export" onSelect={onExportProject} />
        <Action label={t('Import .zip into this project')} sound="import" onSelect={onImportArchive} />
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
        <RadioSubmenu
          label={t('Theme')}
          value={settings.theme}
          options={themeOptions}
          onChange={(theme) => {
            onChangeSettings({ theme, syntax: theme });
          }}
        />
        <RadioSubmenu
          label={t('Syntax colors')}
          value={settings.syntax}
          options={themeOptions}
          onChange={(syntax) => {
            onChangeSettings({ syntax });
          }}
        />
        <RadioSubmenu
          label={t('Language')}
          value={locale}
          options={LOCALES}
          onChange={(nextLocale) => {
            onChangeSettings({ locale: nextLocale });
          }}
        />
        <RadioSubmenu
          label={t('Code font')}
          value={settings.codeFont}
          options={CODE_FONTS}
          onChange={(codeFont) => {
            onChangeSettings({ codeFont });
          }}
        />
        <Menubar.CheckboxItem
          className="menubar-item menubar-radio"
          checked={settings.sound}
          onCheckedChange={(sound) => {
            onChangeSettings({ sound });
          }}>
          <Menubar.ItemIndicator className="menubar-indicator">✓</Menubar.ItemIndicator>
          {t('Sound')}
        </Menubar.CheckboxItem>
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
        <Action label={t('Lessons')} onSelect={onOpenLessons} />
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

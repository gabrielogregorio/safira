import type { Ref } from 'react';

interface ArchiveInputProps {
  ref: Ref<HTMLInputElement>;
  label: string;
  onSelect: (file: File) => void;
}

export const ArchiveInput = ({ ref, label, onSelect }: ArchiveInputProps) => (
  <input
    ref={ref}
    className="archive-input"
    type="file"
    accept=".zip,application/zip"
    aria-label={label}
    tabIndex={-1}
    onChange={(event) => {
      const file = event.target.files?.[0];
      event.target.value = '';

      if (file !== undefined) {
        onSelect(file);
      }
    }}
  />
);

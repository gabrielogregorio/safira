import type { VisionMode } from '@/settings/vision';

const VISION_LABELS = {
  default: 'Default',
  protanopia: 'Protanopia (weak red)',
  deuteranopia: 'Deuteranopia (weak green)',
  tritanopia: 'Tritanopia (weak blue)',
  achromatopsia: 'Achromatopsia (no colors)',
  lowVision: 'Low vision (cataract, glaucoma)',
  lightSensitivity: 'Light sensitivity (migraine, photophobia)',
  calm: 'Epilepsy and dizziness (no motion)',
} as const satisfies Record<VisionMode, string>;

export const visionLabel = <Translated>(
  t: (key: (typeof VISION_LABELS)[VisionMode]) => Translated,
  vision: VisionMode,
): Translated => t(VISION_LABELS[vision]);

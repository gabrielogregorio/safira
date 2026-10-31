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

const VISION_HINTS = {
  default: 'The normal colors of the theme.',
  protanopia: 'For those who see red as weak. Uses blue and orange instead of red and green.',
  deuteranopia: 'For those who see green as weak. Uses blue and orange instead of red and green.',
  tritanopia: 'For those who confuse blue and yellow. Uses colors that do not depend on blue.',
  achromatopsia: 'For those who do not see colors. Uses grays, with bold, italics and underlines to tell things apart.',
  lowVision: 'For those who see little. Solid background, the strongest contrast and no scenery.',
  lightSensitivity: 'For those bothered by light. Dark surfaces and warm tones, in any theme.',
  calm: 'For those bothered by movement. Turns off the animations of the interface.',
} as const satisfies Record<VisionMode, string>;

export const visionHint = <Translated>(
  t: (key: (typeof VISION_HINTS)[VisionMode]) => Translated,
  vision: VisionMode,
): Translated => t(VISION_HINTS[vision]);

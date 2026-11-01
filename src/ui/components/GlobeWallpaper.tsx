import { useIdle } from '@/ui/hooks/useIdle';
import { AeroOrb } from './AeroOrb';
import { CloseButton } from './CloseButton';

const GLOBE_SIZE = 512;

export const GlobeWallpaper = ({ onClose }: { onClose: () => void }) => {
  const isIdle = useIdle();

  return (
    <div className={isIdle ? 'wallpaper is-idle' : 'wallpaper'}>
      <AeroOrb size={GLOBE_SIZE} />
      <CloseButton onClick={onClose} />
    </div>
  );
};

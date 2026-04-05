import { Composition, getInputProps } from 'remotion';
import { CaptionShort } from './CaptionShort';

// Default props if not passed via CLI
const defaultProps = {
    audioUrl: '',
    srtData: [],
    title: 'Elite Mindset',
};

export const RemotionVideo: React.FC = () => {
    return (
        <>
            <Composition
                id="CaptionShort"
                component={CaptionShort}
                durationInFrames={1800} // 60s at 30fps default, but will be dynamic via CLI
                fps={30}
                width={1080}
                height={1920}
                defaultProps={defaultProps}
            />
        </>
    );
};

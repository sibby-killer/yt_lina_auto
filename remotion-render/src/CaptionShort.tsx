import React, { useMemo } from 'react';
import { AbsoluteFill, useVideoConfig, useCurrentFrame, Audio, interpolate, spring, Video, staticFile } from 'remotion';

interface SubtitleProps {
    start: number;
    end: number;
    text: string;
}

export const CaptionShort: React.FC<{
    audioUrl?: string;
    srtData?: SubtitleProps[];
    title?: string;
    bgVideoUrl?: string;
}> = ({ audioUrl, srtData = [], title = "", bgVideoUrl = "" }) => {
    const { fps, width, height } = useVideoConfig();
    const frame = useCurrentFrame();

    // 1-word text isolation
    const currentWord = useMemo(() => {
        const currentTime = frame / fps;
        const currentSub = srtData.find(
            (sub) => currentTime >= sub.start && currentTime <= sub.end
        );
        return currentSub ? currentSub.text : '';
    }, [frame, fps, srtData]);

    // Motion graphic background (simple gradient shift)
    const yOffset = interpolate(frame % 300, [0, 150, 300], [-50, 50, -50], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    // Remove fast pulsating scale to avoid text flickering
    const zoomText = 1;

    return (
        <AbsoluteFill style={{ 
            background: 'linear-gradient(135deg, #0f2027, #203a43, #2c5364)', 
            justifyContent: 'center', 
            alignItems: 'center' 
        }}>
            {/* Scraped B-roll as base layer with low opacity and very low volume */}
            {bgVideoUrl && (
               <AbsoluteFill>
                   <Video src={staticFile(bgVideoUrl)} volume={0.05} style={{ objectFit: 'cover', opacity: 0.3, width: '100%', height: '100%' }} />
               </AbsoluteFill>
            )}

            {/* Animated BG shape mixed with B-roll */}
            <div style={{
                position: 'absolute',
                width: 800,
                height: 800,
                borderRadius: '50%',
                background: 'rgba(255, 255, 255, 0.05)',
                filter: 'blur(100px)',
                transform: `translateY(${yOffset}px)`
            }} />

            {/* Audio Track */}
            {audioUrl && <Audio src={staticFile(audioUrl)} />}

            {/* 1 Word Captions */}
            {currentWord ? (
                <div style={{
                    color: '#fff',
                    fontFamily: 'sans-serif',
                    fontWeight: 900,
                    fontSize: 140,
                    textTransform: 'uppercase',
                    textAlign: 'center',
                    textShadow: '0px 10px 30px rgba(0,0,0,0.8)',
                    transform: `scale(${zoomText})`,
                    zIndex: 10
                }}>
                    {currentWord}
                </div>
            ) : (
                <div style={{
                    color: 'rgba(255,255,255,0.2)',
                    fontFamily: 'sans-serif',
                    fontWeight: 700,
                    fontSize: 80,
                    textAlign: 'center',
                    textTransform: 'uppercase',
                    width: '80%',
                    zIndex: 10
                }}>
                    {title}
                </div>
            )}
        </AbsoluteFill>
    );
};

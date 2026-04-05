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

    // 2-word text chunking with gap bridging
    const currentChunkInfo = useMemo(() => {
        const currentTime = frame / fps;
        
        for (let i = 0; i < srtData.length; i += 2) {
            const word1 = srtData[i];
            const word2 = srtData[i + 1];
            
            const start = word1.start;
            // Bridge the gap up to 0.2 seconds between words
            const end = word2 ? word2.end : word1.end;
            
            if (currentTime >= start - 0.05 && currentTime <= end + 0.1) {
                return {
                    words: word2 ? [word1.text, word2.text] : [word1.text],
                    startFrame: Math.floor(start * fps)
                };
            }
        }
        return null;
    }, [frame, fps, srtData]);

    // Motion graphic background (simple gradient shift)
    const yOffset = interpolate(frame % 300, [0, 150, 300], [-50, 50, -50], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
    });

    // Pop animation based on the start frame of the 2-word chunk
    const popScale = currentChunkInfo ? spring({
        fps,
        frame: frame - currentChunkInfo.startFrame,
        config: { damping: 15, mass: 0.5, stiffness: 200 },
        durationInFrames: 10,
    }) : 0;
    
    // Slight continuous scale mapping mapping from 1.0 to 1.1 based on lifetime of chunk
    const zoomText = currentChunkInfo ? 1 + ((frame - currentChunkInfo.startFrame) * 0.005) : 1;
    const finalScale = currentChunkInfo ? popScale * zoomText : 0;

    return (
        <AbsoluteFill style={{ 
            background: '#0a0a0a', 
            justifyContent: 'center', 
            alignItems: 'center' 
        }}>
            {/* Scraped B-roll as base layer with low opacity and very low volume */}
            {bgVideoUrl && (
               <AbsoluteFill>
                   <Video src={staticFile(bgVideoUrl)} volume={0.05} style={{ objectFit: 'cover', opacity: 0.4, width: '100%', height: '100%' }} />
               </AbsoluteFill>
            )}

            {/* Simulated Vignette / Shadow Overlay */}
            <AbsoluteFill style={{
                background: 'radial-gradient(circle, rgba(0,0,0,0) 40%, rgba(0,0,0,0.8) 100%)',
            }} />

            {/* Audio Track */}
            {audioUrl && <Audio src={staticFile(audioUrl)} />}

            {/* 2-Word Dynamic Captions with Typography and Motion */}
            {currentChunkInfo && (
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    gap: '30px',
                    fontFamily: "'Inter', 'Montserrat', sans-serif",
                    fontWeight: 900,
                    fontSize: 150,
                    textTransform: 'uppercase',
                    textAlign: 'center',
                    transform: `scale(${finalScale})`,
                    zIndex: 10
                }}>
                    <span style={{ 
                        color: '#ffffff', 
                        textShadow: '0px 15px 40px rgba(0,0,0,0.9), 0px 5px 10px rgba(0,0,0,0.8)' 
                    }}>
                        {currentChunkInfo.words[0]}
                    </span>
                    {currentChunkInfo.words[1] && (
                        <span style={{ 
                            color: '#ff2a2a', // High energy red accent
                            textShadow: '0px 15px 40px rgba(0,0,0,0.9), 0px 5px 10px rgba(0,0,0,0.8)' 
                        }}>
                            {currentChunkInfo.words[1]}
                        </span>
                    )}
                </div>
            )}
        </AbsoluteFill>
    );
};

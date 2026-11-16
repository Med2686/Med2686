import { Composition } from "remotion";
import { CLEAN_TOTAL, CleanCut } from "./CleanCut";

export const RemotionRoot: React.FC = () => (
  <>
    {/* the clean cut alone: the user checks every cut by ear here before any effect. Render ONLY on his OK. */}
    <Composition id="CleanCut" component={CleanCut} durationInFrames={CLEAN_TOTAL} fps={30} width={1080} height={1920} defaultProps={{ labels: true }} />
  </>
);

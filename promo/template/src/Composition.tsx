import React from "react";
import { AbsoluteFill, Sequence, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { Audio, Video } from "@remotion/media";
import timeline from "./timeline.json";
import reelData from "./reel.json";

export const FPS = 30;
const tl = timeline as any;
const R = reelData as any;
// Every colour lives here (hallmark floor 1): change the palette in one place.
const C = {
  bg: "#1a1a2e", bgHi: "#2a2a52", panel: "#25254a", term: "#0e0e1c", termBar: "#1d1d38", termLine: "#3a3a60",
  stage: "#0b0b16", frame: "#55557a", text: "#ffffff", textSoft: "#e8e8f5", muted: "#9a9bb8", mutedHi: "#cfd0e6",
  paper: "#e6e6f0", pageEdge: "#aaaabb", gold: "#f5c518", teal: "#16c79a", red: "#e94560", pink: "#ff7b93",
  capBg: "rgba(8,8,22,0.78)", dim: "rgba(255,255,255,0.45)", shadow: "rgba(0,0,0,0.55)",
};
const COL: Record<string, string> = { gold: C.gold, teal: C.teal, red: C.red, white: C.text };
// Offset drop shadow only; no zero-offset coloured glow (hallmark gate 29).
const LIFT = `0 8px 30px ${C.shadow}`;
const at = (a: [string, number]) => L(a[0]).phrases[a[1]].start;
export const TOTAL = Math.ceil(tl.total * FPS);
const NAVY = C.bg, GOLD = C.gold, TEAL = C.teal, RED = C.red, PANEL = C.panel;
const FONT = "'Apple SD Gothic Neo', 'AppleSDGothicNeo', sans-serif";
const MONO = "Menlo, 'Apple SD Gothic Neo', monospace";
const lines: any[] = tl.lines;
const SC = tl.scenes;
const L = (id: string) => lines.find((l) => l.id === id);
const clampI = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const sp = (t: number, t0: number, _d = 13, _s = 170) =>
  t < t0 ? 0 : spring({ frame: (t - t0) * FPS, fps: FPS, config: { damping: 26, stiffness: 120 } });
const curPhrase = (id: string, t: number) => {
  const ps = L(id).phrases; let k = -1;
  ps.forEach((p: any, i: number) => { if (t >= p.start) k = i; });
  return k;
};

const bgStyle: React.CSSProperties = { background: `radial-gradient(circle at 50% 28%, ${C.bgHi}, ${NAVY} 72%)` };

const Scene: React.FC<{ name: string; z: number; t: number; slide?: boolean; children: (t: number) => React.ReactNode }> = ({ name, z, t, slide = true, children }) => {
  const s = SC[name];
  if (t < s.from_ || t >= s.to + 0.4) return null;
  const e = slide ? 1 - Math.pow(1 - interpolate(t, [s.from_, s.from_ + 0.28], [0, 1], clampI), 3) : 1;
  const punch = 1;
  return (
    <AbsoluteFill style={{ ...bgStyle, zIndex: z, transform: `translateX(${(1 - e) * 1080}px)` }}>
      <AbsoluteFill style={{ transform: `scale(${punch})` }}>{children(t - s.from_)}</AbsoluteFill>
    </AbsoluteFill>
  );
};

const Abs: React.FC<{ top: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ top, children, style }) => (
  <div style={{ position: "absolute", top, left: 54, width: 972, display: "flex", flexDirection: "column", alignItems: "center", ...style }}>{children}</div>
);

/* ---------- 1 HOOK ---------- */
const Hook: React.FC<{ t: number }> = ({ t }) => {
  const ids = Object.keys(R.hook); const id = [...ids].reverse().find((k) => t >= L(k).start) ?? ids[0];
  const t0 = L(id).start;
  return (
    <AbsoluteFill>
      <Abs top={270}>
        {R.hook[id].map(([txt, c0]: [string, string], i: number) => { const col = COL[c0];
          const s = sp(t, t0 + i * 0.12, 11, 260);
          return <div key={id + i} style={{ fontSize: 116, fontWeight: 900, color: col, lineHeight: 1.18, opacity: s, transform: `translateY(${(1 - s) * 40}px)`, textShadow: LIFT }}>{txt}</div>;
        })}
      </Abs>
      <div style={{ position: "absolute", left: 180, width: 720, top: 800, height: 12, borderRadius: 6, background: id === ids[0] ? RED : TEAL, transform: `scaleX(${sp(t, t0 + 0.4)})` }} />
    </AbsoluteFill>
  );
};

/* ---------- 2 PAIN ---------- */
const PainCard: React.FC<{ i: number; t: number; t0: number }> = ({ i, t, t0 }) => {
  const s = sp(t, t0, 15, 200);
  const col = COL[R.pain[i].color];
  const label = R.pain[i].label;
  const vis = R.pain[i].visual;
  const bars = Array.from({ length: 22 });
  return (
    <AbsoluteFill style={{ ...bgStyle, transform: `translateX(${(1 - s) * 1080}px)` }}>
      <Abs top={230}><div style={{ fontSize: 92, fontWeight: 900, color: col }}>{label}</div></Abs>
      {vis === "pages" && (
        <div style={{ position: "absolute", top: 420, left: 90, width: 900, display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: 16 }}>
          {Array.from({ length: 30 }).map((_, k) => {
            const q = sp(t, t0 + k * 0.012, 14);
            return <div key={k} style={{ height: 120, borderRadius: 10, background: C.text, opacity: 0.92 * q, transform: `scale(${q}) rotate(${(k % 5 - 2) * 2}deg)`, borderTop: `18px solid ${k % 4 === 0 ? GOLD : C.pageEdge}` }} />;
          })}
        </div>
      )}
      {vis === "wave" && (
        <div style={{ position: "absolute", top: 450, left: 70, width: 940, height: 520, display: "flex", alignItems: "center", gap: 12 }}>
          {bars.map((_, k) => (
            <div key={k} style={{ flex: 1, borderRadius: 10, background: GOLD, height: 440, scale: `1 ${(60 + 380 * Math.abs(Math.sin(t * 3 + k * 0.9)) * (0.4 + 0.6 * Math.abs(Math.sin(k * 1.7)))) / 440}` }} />
          ))}
        </div>
      )}
      {vis === "calendar" && (
        <>
          <div style={{ position: "absolute", top: 440, left: 190, width: 700, height: 560, borderRadius: 30, background: C.text, overflow: "hidden" }}>
            <div style={{ height: 140, background: RED }} />
            <div style={{ display: "grid", gridTemplateColumns: "repeat(5,1fr)", gap: 14, padding: 30 }}>
              {Array.from({ length: 20 }).map((_, k) => <div key={k} style={{ height: 58, borderRadius: 8, background: k === 13 ? RED : C.paper }} />)}
            </div>
          </div>
          <div style={{ position: "absolute", top: 860, left: 690, fontSize: 260, fontWeight: 900, color: RED, textShadow: LIFT, transform: "rotate(12deg)" }}>!</div>
        </>
      )}
    </AbsoluteFill>
  );
};
const Pain: React.FC<{ t: number; gt: number }> = ({ t, gt }) => {
  const k = Math.max(0, curPhrase("pain", gt));
  const ps = L("pain").phrases;
  const t0 = SC.pain.from_;
  return <AbsoluteFill>{R.pain.map((_: any, i: number) => i).filter((i: number) => i <= k).map((i: number) => <PainCard key={i} i={i} t={gt} t0={i === 0 ? t0 : ps[i].start} />)}</AbsoluteFill>;
};

/* ---------- 3 REVEAL ---------- */
const Reveal: React.FC<{ t: number }> = ({ t }) => {
  const a = sp(t, 0.05, 11, 220), b = sp(t, 0.45, 12, 200);
  return (
    <AbsoluteFill>
      {[0, 1, 2].map((i) => {
        const r = ((t * 0.9 + i / 3) % 1);
        return <div key={i} style={{ position: "absolute", left: 540 - 420 * r, top: 560 - 420 * r, width: 840 * r, height: 840 * r, borderRadius: "50%", border: `5px solid ${TEAL}`, opacity: (1 - r) * 0.5 * Math.min(1, a) }} />;
      })}
      <Abs top={400}>
        <div style={{ fontFamily: MONO, fontSize: 132, fontWeight: 900, color: GOLD, transform: `scale(${0.4 + 0.6 * a})`, opacity: Math.min(1, a * 2), textShadow: LIFT }}>{R.brand.name}</div>
        <div style={{ marginTop: 50, padding: "18px 50px", borderRadius: 60, background: TEAL, color: NAVY, fontSize: 64, fontWeight: 900, transform: `scale(${b})`, opacity: b, boxShadow: LIFT }}>{R.brand.badge}</div>
      </Abs>
    </AbsoluteFill>
  );
};

/* ---------- 4 DEMO (terminal) ---------- */
const CMD: string = R.terminal.command;
const Demo: React.FC<{ t: number; gt: number }> = ({ t, gt }) => {
  const from = SC.demo.from_;
  const n = Math.floor(interpolate(gt, [from + 0.1, from + 0.75], [0, CMD.length], clampI));
  const times: number[] = R.terminal.steps.map((s: any) => at(s.at));
  const dl = L(R.terminal.doneAfterLine);
  const done = dl.start + dl.dur;
  const steps: string[] = R.terminal.steps.map((s: any) => s.text);
  const s = sp(t, 0, 16, 160);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 60, top: 300, width: 960, height: 880, borderRadius: 28, background: C.term, border: `3px solid ${C.termLine}`, overflow: "hidden", transform: `scale(${0.85 + 0.15 * s})`, opacity: s, boxShadow: `0 30px 80px ${C.shadow}` }}>
        {/* No drawn traffic-light buttons (hallmark floor 11 / gate 47a): only the "예시 화면" disclaimer. */}
        <div style={{ height: 70, background: C.termBar, display: "flex", alignItems: "center", padding: "0 26px" }}>
          <div style={{ marginLeft: "auto", padding: "6px 20px", borderRadius: 20, border: `2px solid ${GOLD}`, color: GOLD, fontSize: 28, fontWeight: 800 }}>{R.terminal.label}</div>
        </div>
        <div style={{ padding: "36px 36px", fontFamily: MONO, fontSize: 36, color: C.textSoft, lineHeight: 1.5 }}>
          <div style={{ color: TEAL, whiteSpace: "pre" }}>{CMD.slice(0, n)}{gt < from + 1.0 && Math.floor(gt * 4) % 2 === 0 ? "▌" : ""}</div>
          <div style={{ height: 24 }} />
          {steps.map((st, i) => {
            if (gt < times[i]) return null;
            const fin = i < steps.length - 1 ? gt >= times[i + 1] : gt >= done;
            const a = sp(gt, times[i], 14, 220);
            return (
              <div key={i} style={{ marginBottom: 26, opacity: a, transform: `translateX(${(1 - a) * 60}px)`, color: fin ? C.textSoft : GOLD }}>
                <span style={{ color: fin ? TEAL : GOLD, fontWeight: 900 }}>{fin ? "✓" : "◐"}</span> {st}{fin ? "" : "…"}
              </div>
            );
          })}
          {gt >= done && <div style={{ marginTop: 40, display: "flex", alignItems: "center", gap: 20, fontSize: 64, fontWeight: 900, color: TEAL, transform: `scale(${sp(gt, done, 9, 240)})`, transformOrigin: "left center" }}><Check size={72} progress={1} />{R.terminal.done}</div>}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 4b PROOF (laptop with real clips) ---------- */
const Proof: React.FC<{ t: number }> = ({ t }) => {
  const s = SC.proof; const len = s.to - s.from_;
  const k = interpolate(t, [0.1, 0.9], [0, 1], clampI);
  const a = sp(t, 0.1, 13, 200), b = sp(t, 0.25, 13, 200);
  const seg = Math.round((len * FPS) / R.proof.clips.length);
  return (
    <AbsoluteFill>
      <Abs top={215}><div style={{ fontSize: 84, fontWeight: 900, color: C.text, transform: `scale(${a})` }}>{R.proof.number1.format.split("{n}")[0]}<span style={{ color: GOLD, fontSize: 120 }}>{Math.round(R.proof.number1.value * k)}</span>{R.proof.number1.format.split("{n}")[1]}</div></Abs>
      <Abs top={370}><div style={{ fontSize: 92, fontWeight: 900, color: TEAL, transform: `scale(${b})` }}>{R.proof.number2.format.split("{n}")[0]}{Math.round(R.proof.number2.value * k)}{R.proof.number2.format.split("{n}")[1]}</div></Abs>
      <div style={{ position: "absolute", left: 50, top: 560, width: 980, height: 520, borderRadius: 30, background: C.stage, border: `6px solid ${C.frame}`, transform: `scale(${sp(t, 0.15, 14, 150)})` }}>
        <div style={{ position: "absolute", left: 20, top: 20, width: 940, height: 454, borderRadius: 12, overflow: "hidden", background: NAVY }}>
          {(R.proof.clips as string[]).map((c, i, arr) => (
            <Sequence key={c} from={Math.round(s.from_ * FPS) + i * seg} durationInFrames={i === arr.length - 1 ? 9999 : seg}>
              <Video src={staticFile(c)} muted objectFit="cover" style={{ width: 940, height: 454 }} />
            </Sequence>
          ))}
        </div>
      </div>
      <div style={{ position: "absolute", left: 20, top: 1086, width: 1040, height: 16, borderRadius: 8, background: C.frame }} />
      <Abs top={1125}><div style={{ fontSize: 30, color: C.muted }}>{R.proof.note}</div></Abs>
    </AbsoluteFill>
  );
};

/* ---------- 5 FEATURES ---------- */
// Drawn check (no emoji as an icon, hallmark floor 11 / gate 30a). progress 0..1 draws the stroke.
const Check: React.FC<{ size: number; progress: number }> = ({ size, progress }) => (
  <svg width={size} height={size} viewBox="0 0 96 96"><circle cx="48" cy="48" r="44" fill={TEAL} /><path d="M26 50 L42 66 L72 32" fill="none" stroke={C.text} strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" strokeDasharray="90" strokeDashoffset={90 * (1 - progress)} /></svg>
);
const Feat: React.FC<{ gt: number }> = ({ gt }) => {
  const PILLS = R.pills as any[];
  const times = PILLS.map((p) => at(p.at));
  return (
    <AbsoluteFill>
      {PILLS.map((p, i) => { const txt = p.text, col = COL[p.color];
        const s = sp(gt, times[i], 12, 220);
        const ck = interpolate(gt, [times[i] + 0.1, times[i] + 0.3], [0, 1], clampI);
        return (
          <div key={i} style={{ position: "absolute", left: 60, top: 245 + i * 175, width: 960, height: 145, borderRadius: 72, background: PANEL, border: `6px solid ${col}`, display: "flex", alignItems: "center", padding: "0 34px", gap: 28, opacity: Math.min(1, s * 2), transform: `translateX(${(1 - s) * (i % 2 ? 900 : -900)}px) scale(${0.9 + 0.1 * s})` }}>
            <Check size={80} progress={ck} />
            <div style={{ fontSize: 42, fontWeight: 900, color: C.text }}>{txt}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------- 6 CTA ---------- */
const HEART = "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z";
const Cta: React.FC<{ t: number; gt: number }> = ({ t, gt }) => {
  const c2 = L(R.cta.heartLine).phrases;
  const th = c2[0].start, tf = c2[1].start;
  const pill = (txt: string, col: string, d: number) => {
    const s = sp(t, d, 12, 220);
    return <div style={{ padding: "12px 32px", borderRadius: 50, background: col, color: NAVY, fontSize: 48, fontWeight: 900, transform: `scale(${s})`, opacity: s }}>{txt}</div>;
  };
  const hs = sp(gt, th, 8, 200);
  const beat = 1 + 0.08 * Math.abs(Math.sin((gt - th) * 3));
  const press = gt > tf + 0.5 ? 1 - 0.1 * Math.exp(-(gt - tf - 0.5) * 12) * 1 : 1;
  const fs = sp(gt, tf, 10, 220);
  return (
    <AbsoluteFill>
      <Abs top={225} style={{ flexDirection: "row", justifyContent: "center", gap: 16 }}>{R.cta.pills.map(([tx, cl]: [string, string], i: number) => pill(tx, COL[cl], i * 0.1))}</Abs>
      <Abs top={355}><div style={{ fontSize: 48, fontWeight: 800, color: C.text, opacity: sp(t, 0.2) }}>{R.cta.url}</div></Abs>
      <Abs top={460}><div style={{ padding: "22px 44px", borderRadius: 24, background: C.term, border: `4px solid ${TEAL}`, fontFamily: MONO, fontSize: 56, fontWeight: 900, color: TEAL, transform: `scale(${0.7 + 0.3 * sp(t, 0.3)})`, opacity: sp(t, 0.3) }}>{R.cta.command} <span style={{ color: GOLD }}>{R.cta.commandAccent}</span></div></Abs>
      <Abs top={620}><div style={{ fontSize: 28, color: C.muted, opacity: sp(t, 0.4) }}>{R.cta.small}</div></Abs>
      <Abs top={690}><div style={{ fontSize: 46, fontWeight: 900, color: C.text, opacity: sp(t, 0.5) }}>{R.cta.save[0]}<span style={{ color: GOLD }}>{R.cta.save[1]}</span>{R.cta.save[2]}</div></Abs>
      {gt >= th && Array.from({ length: 7 }).map((_, k) => {
        const age = (gt - th - k * 0.18);
        if (age < 0) return null;
        const r = (age % 1.3) / 1.3;
        return <svg key={k} width="60" height="60" viewBox="0 0 24 24" style={{ position: "absolute", left: 300 + ((k * 137) % 480), top: 960, translate: `0px ${-r * 260}px`, opacity: (1 - r) * 0.8 }}><path d={HEART} fill={k % 2 ? RED : C.pink} /></svg>;
      })}
      <div style={{ position: "absolute", left: 440, top: 790, width: 200, height: 200, transform: `scale(${hs * beat})`, opacity: Math.min(1, hs * 2) }}>
        <svg width="200" height="200" viewBox="0 0 24 24"><path d={HEART} fill={RED} /></svg>
      </div>
      <div style={{ position: "absolute", left: 0, width: 1080, top: 1040, display: "flex", justifyContent: "center", transform: `scale(${fs * press})`, opacity: Math.min(1, fs * 2) }}>
        <div style={{ padding: "14px 60px", borderRadius: 60, background: GOLD, color: NAVY, fontSize: 60, fontWeight: 900 }}>{R.cta.followText}</div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- karaoke caption ---------- */
const Caption: React.FC<{ t: number }> = ({ t }) => {
  let li = -1; lines.forEach((l, i) => { if (t >= l.start - 0.04) li = i; });
  if (li < 0) return null;
  const l = lines[li];
  const s = sp(t, l.start - 0.04, 16, 260);
  return (
    <div style={{ position: "absolute", left: 40, width: 1000, top: 1250, height: 190, display: "flex", alignItems: "center", justifyContent: "center", opacity: Math.min(1, s * 2), transform: `translateY(${(1 - s) * 24}px)` }}>
      <div style={{ background: C.capBg, padding: "10px 30px", borderRadius: 22, textAlign: "center" }}>
        {l.rows.map((row: string[], ri: number) => (
          <div key={ri} style={{ fontSize: 62, fontWeight: 900, lineHeight: 1.3, whiteSpace: "pre" }}>
            {row.filter((p) => p.trim()).map((p, pi) => {
              const ph = l.phrases.find((x: any) => x.row === ri && x.text === p);
              const cur = t >= ph.start && t < ph.end + 0.0001 || (t >= ph.start && ph === l.phrases[l.phrases.length - 1] && t < l.start + l.dur + 0.3);
              const past = t >= ph.end;
              return <span key={pi} style={{ color: cur ? GOLD : past ? C.text : C.dim }}>{p}</span>;
            })}
          </div>
        ))}
      </div>
    </div>
  );
};

export const Reel: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  return (
    <AbsoluteFill style={{ background: NAVY, fontFamily: FONT, overflow: "hidden" }}>
      <Scene name="hook" z={1} t={t} slide={false}>{(lt) => <Hook t={t} />}</Scene>
      <Scene name="pain" z={2} t={t}>{(lt) => <Pain t={lt} gt={t} />}</Scene>
      <Scene name="reveal" z={3} t={t}>{(lt) => <Reveal t={lt} />}</Scene>
      <Scene name="demo" z={4} t={t}>{(lt) => <Demo t={lt} gt={t} />}</Scene>
      <Scene name="proof" z={5} t={t}>{(lt) => <Proof t={lt} />}</Scene>
      <Scene name="feat" z={6} t={t}>{(lt) => <Feat gt={t} />}</Scene>
      <Scene name="cta" z={7} t={t}>{(lt) => <Cta t={lt} gt={t} />}</Scene>
      <div style={{ position: "absolute", inset: 0, zIndex: 20 }}><Caption t={t} /></div>
      {lines.map((l) => (
        <Sequence key={l.id} from={Math.round(l.start * FPS)} durationInFrames={Math.round(l.dur * FPS) + 4}><Audio src={staticFile(`tts/${l.id}.mp3`)} /></Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const Cover: React.FC = () => (
  <AbsoluteFill style={{ ...bgStyle, fontFamily: FONT }}>
    <Abs top={300}>
      <div style={{ fontFamily: MONO, fontSize: 118, fontWeight: 900, color: GOLD, textShadow: LIFT }}>{R.brand.name}</div>
      <div style={{ marginTop: 36, padding: "14px 44px", borderRadius: 50, background: TEAL, color: NAVY, fontSize: 52, fontWeight: 900 }}>{R.brand.badge}</div>
      <div style={{ fontSize: 96, fontWeight: 900, color: C.text, textAlign: "center", marginTop: 70, lineHeight: 1.3 }}>
        {R.cover.lines.map((ln: string, i: number) => <div key={i} style={{ color: i === R.cover.accentLine ? TEAL : C.text }}>{ln}</div>)}
      </div>
      <div style={{ fontSize: 44, color: C.mutedHi, marginTop: 50 }}>{R.cover.sub}</div>
    </Abs>
  </AbsoluteFill>
);

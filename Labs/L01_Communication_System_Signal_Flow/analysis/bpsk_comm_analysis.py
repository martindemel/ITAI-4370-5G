#!/usr/bin/env python3
"""
Digital Communication System — BPSK signal-flow analysis
========================================================
Part 1: Conceptual block diagram  -> comm_system_block_diagram.{png,svg}
Part 2: Signal-flow analysis       -> bpsk_signal_flow.png
                                      bpsk_constellation.png
                                      bpsk_ber_curve.{png,svg}

Chain modelled:
    Source (bits) -> BPSK Modulator -> AWGN Channel -> Demodulator -> Receiver (bits)

Conventions
-----------
BPSK mapping : bit 0 -> symbol -1 , bit 1 -> symbol +1   (Eb = 1)
AWGN channel : r = s + n , real baseband, n ~ N(0, N0/2)
              with Eb/N0 (linear) = g  ->  N0 = 1/g , sigma = sqrt(1/(2g))
Demodulator  : matched filter + threshold ->  r > 0 -> 1 , else 0
Theory       : Pb = 0.5 * erfc( sqrt(Eb/N0) )    [exact for coherent BPSK]

Light mode only. No external assets, no network.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.special import erfc

OUT = "/mnt/user-data/outputs"

# ----------------------------------------------------------------------
# Global light-mode styling
# ----------------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#1A1A1A",
    "text.color": "#1A1A1A",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.grid": True,
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.8,
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "legend.framealpha": 0.95,
    "legend.edgecolor": "#CCCCCC",
})

# Shared palette (matches the block diagram colours)
C_BITS   = "#1565C0"   # blue   - source / receiver
C_MOD    = "#2E7D32"   # green  - modulator / symbols
C_CHAN   = "#E65100"   # orange - channel / noise
C_THEORY = "#37474F"   # slate  - theoretical reference
C_GRIDLN = "#9E9E9E"


# ======================================================================
# PART 1 — Conceptual block diagram (matplotlib render of the .drawio)
# ======================================================================
def draw_block_diagram(png_path, svg_path):
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # (label, x-left, fill, edge)
    boxes = [
        ("Source\n(Bits)",   0.5,  "#dae8fc", C_BITS),
        ("BPSK\nModulator",  3.0,  "#d5e8d4", C_MOD),
        ("Channel\n(AWGN)",  5.5,  "#ffe6cc", C_CHAN),
        ("Demodulator",      8.0,  "#d5e8d4", C_MOD),
        ("Receiver\n(Bits)", 10.5, "#dae8fc", C_BITS),
    ]
    bw, bh, by = 2.0, 1.1, 2.0
    spans = []
    for label, x, fc, ec in boxes:
        ax.add_patch(FancyBboxPatch(
            (x, by), bw, bh,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=2.2, edgecolor=ec, facecolor=fc, mutation_aspect=1))
        ax.text(x + bw / 2, by + bh / 2, label, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color="#1A1A1A")
        spans.append((x, x + bw))

    # left-to-right signal arrows + labels
    edge_labels = ["bits b[n]", "s(t)", "r(t) = s(t) + n(t)", "recovered bits"]
    ymid = by + bh / 2
    for i in range(4):
        x0, x1 = spans[i][1], spans[i + 1][0]
        ax.add_patch(FancyArrowPatch((x0, ymid), (x1, ymid),
                     arrowstyle="-|>", mutation_scale=20,
                     linewidth=2.2, color="#37474F"))
        ax.text((x0 + x1) / 2, ymid + 0.30, edge_labels[i],
                ha="center", va="bottom", fontsize=9.5, color="#37474F")

    # noise source feeding the channel
    nx, ny, nw, nh = 5.75, 3.65, 1.5, 0.8
    ax.add_patch(FancyBboxPatch(
        (nx, ny), nw, nh,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        linewidth=1.8, edgecolor="#d6b656", facecolor="#fff2cc", linestyle="--"))
    ax.text(nx + nw / 2, ny + nh / 2, "Noise n(t)\n(AWGN)",
            ha="center", va="center", fontsize=10, color="#7a5c00")
    ch_cx = 5.5 + bw / 2
    ax.add_patch(FancyArrowPatch((nx + nw / 2, ny), (ch_cx, by + bh),
                 arrowstyle="-|>", mutation_scale=16,
                 linewidth=1.8, color=C_CHAN, linestyle="--"))
    ax.text(ch_cx + 1.05, (ny + by + bh) / 2, "noise added\nin channel",
            ha="left", va="center", fontsize=8.8, color=C_CHAN)

    # stage annotations
    ax.text(3.0 + bw / 2, by - 0.42, "BPSK:  0 \u2192 \u22121,  1 \u2192 +1",
            ha="center", va="top", fontsize=9.2, color=C_MOD)
    ax.text(8.0 + bw / 2, by - 0.42, "decision:  r > 0 \u2192 1, else 0",
            ha="center", va="top", fontsize=9.2, color=C_MOD)

    ax.text(6.5, 4.65, "Digital Communication System \u2014 BPSK Signal Flow",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#1A1A1A")

    fig.tight_layout()
    fig.savefig(png_path, dpi=150, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[part1] block diagram -> {png_path} , {svg_path}")


# ======================================================================
# PART 2 — Signal-flow analysis
# ======================================================================

def bpsk_modulate(bits):
    """bit 0 -> -1 , bit 1 -> +1  (Eb = 1)."""
    return 2.0 * bits - 1.0


def awgn(symbols, ebn0_db, rng):
    """Add real AWGN at the requested Eb/N0 (dB). Eb assumed = 1."""
    g = 10.0 ** (ebn0_db / 10.0)          # Eb/N0 linear
    sigma = np.sqrt(1.0 / (2.0 * g))      # N0/2 variance -> std
    return symbols + sigma * rng.standard_normal(symbols.shape)


def demodulate(r):
    """Matched-filter output already in r; threshold at zero."""
    return (r > 0).astype(int)


# ---------- 2a. Signal-flow demo (short, human-readable) --------------
def figure_signal_flow(path):
    N_DEMO = 12
    EBN0_DEMO = 1.0          # low SNR so a bit error is visible in the demo
    sps = 200               # samples per bit for the passband waveform
    fc = 2.0                # carrier cycles per bit

    # find a seed giving exactly 1-2 errors among N_DEMO bits (clear teaching figure)
    chosen = None
    for seed in range(500):
        rng = np.random.default_rng(seed)
        bits = rng.integers(0, 2, N_DEMO)
        sym = bpsk_modulate(bits)
        r = awgn(sym, EBN0_DEMO, rng)
        bhat = demodulate(r)
        nerr = int(np.sum(bhat != bits))
        if 1 <= nerr <= 2:
            chosen = (seed, bits, sym, r, bhat, nerr)
            break
    seed, bits, sym, r, bhat, nerr = chosen
    err_idx = np.where(bhat != bits)[0]

    # passband transmitted waveform
    t = np.arange(N_DEMO * sps) / sps
    carrier = np.cos(2 * np.pi * fc * t)
    sym_up = np.repeat(sym, sps)
    s_pp = sym_up * carrier

    fig, ax = plt.subplots(5, 1, figsize=(12, 11))
    idx = np.arange(N_DEMO)

    # (a) source bits
    ax[0].stem(idx, bits, basefmt=" ", linefmt=C_BITS, markerfmt="o")
    ax[0].set_title("(a) Source — transmitted bits  b[n]")
    ax[0].set_ylim(-0.2, 1.3)
    ax[0].set_yticks([0, 1])
    for i, b in enumerate(bits):
        ax[0].text(i, b + 0.10, str(b), ha="center", va="bottom",
                   fontsize=9, color=C_BITS, fontweight="bold")

    # (b) BPSK baseband symbols
    ax[1].step(np.append(idx, N_DEMO), np.append(sym, sym[-1]),
               where="post", color=C_MOD, linewidth=2)
    ax[1].axhline(0, color=C_GRIDLN, linewidth=0.8)
    ax[1].set_title("(b) BPSK Modulator — baseband symbols  a[n] \u2208 {\u22121, +1}")
    ax[1].set_ylim(-1.6, 1.6)
    ax[1].set_yticks([-1, 0, 1])

    # (c) passband transmitted waveform (phase reversals at bit changes)
    ax[2].plot(t, s_pp, color=C_MOD, linewidth=1.3)
    for k in range(1, N_DEMO):
        ax[2].axvline(k, color="#E0E0E0", linewidth=0.8)
    ax[2].set_title("(c) Transmitted passband signal  s(t) = a[n]\u00b7cos(2\u03c0 f_c t)  — 180\u00b0 phase flips encode bits")
    ax[2].set_ylim(-1.5, 1.5)

    # (d) received matched-filter samples r[n] = a[n] + n[n]  (channel adds AWGN)
    markerline, stemline, _ = ax[3].stem(idx, r, basefmt=" ",
                                         linefmt=C_CHAN, markerfmt="o")
    plt.setp(markerline, color=C_CHAN)
    ax[3].axhline(0, color=C_THEORY, linewidth=1.4, linestyle="--",
                  label="decision threshold")
    ax[3].scatter(err_idx, r[err_idx], s=180, facecolors="none",
                  edgecolors="red", linewidths=2.2, zorder=5,
                  label="bit error")
    ax[3].set_title(f"(d) AWGN Channel + Demodulator — received samples  r[n] = a[n] + n[n]   "
                    f"(Eb/N0 = {EBN0_DEMO:.0f} dB, {nerr} error"
                    f"{'s' if nerr != 1 else ''})")
    ax[3].set_ylim(min(-1.8, r.min() - 0.3), max(1.8, r.max() + 0.3))
    ax[3].legend(loc="upper right", fontsize=9)

    # (e) recovered bits vs original
    ax[4].stem(idx, bhat, basefmt=" ", linefmt=C_BITS, markerfmt="o")
    if len(err_idx):
        ax[4].scatter(err_idx, bhat[err_idx], s=180, facecolors="none",
                      edgecolors="red", linewidths=2.2, zorder=5,
                      label="differs from b[n]")
        ax[4].legend(loc="upper right", fontsize=9)
    ax[4].set_title("(e) Receiver — recovered bits  $\\hat{b}[n]$  (errors circled red)")
    ax[4].set_ylim(-0.2, 1.3)
    ax[4].set_yticks([0, 1])
    ax[4].set_xlabel("bit index  n")

    for a in ax:
        a.set_xlim(-0.5, N_DEMO - 0.5 if a is not ax[2] else N_DEMO)
    ax[2].set_xlim(0, N_DEMO)

    fig.suptitle("BPSK Signal Flow:  Source \u2192 Modulator \u2192 Channel \u2192 Demodulator \u2192 Receiver",
                 fontsize=14, fontweight="bold", y=0.997)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[part2] signal-flow demo -> {path}  (seed={seed}, errors={nerr})")


# ---------- 2b. Constellation diagram ---------------------------------
def figure_constellation(path, ebn0_db=8.0, n=2000):
    rng = np.random.default_rng(7)
    bits = rng.integers(0, 2, n)
    sym = bpsk_modulate(bits).astype(complex)        # signal on the I axis
    g = 10.0 ** (ebn0_db / 10.0)
    sigma = np.sqrt(1.0 / (2.0 * g))                 # per-component std
    noise = sigma * (rng.standard_normal(n) + 1j * rng.standard_normal(n))
    r = sym + noise

    fig, ax = plt.subplots(figsize=(7.2, 7.0))
    ax.scatter(r.real, r.imag, s=10, alpha=0.30, color=C_CHAN,
               label=f"received samples (Eb/N0 = {ebn0_db:.0f} dB)")
    ax.scatter([-1, 1], [0, 0], s=220, color=C_MOD, marker="X",
               edgecolors="white", linewidths=1.5, zorder=5,
               label="ideal TX symbols (\u00b11)")
    ax.axvline(0, color=C_THEORY, linewidth=1.6, linestyle="--",
               label="decision boundary")
    ax.axhline(0, color=C_GRIDLN, linewidth=0.8)
    ax.text(1.0, 0.0, "  bit 1", color=C_MOD, fontsize=11, fontweight="bold",
            va="bottom", ha="left")
    ax.text(-1.0, 0.0, "bit 0  ", color=C_MOD, fontsize=11, fontweight="bold",
            va="bottom", ha="right")
    ax.set_title(f"BPSK Constellation Diagram  (Eb/N0 = {ebn0_db:.0f} dB)")
    ax.set_xlabel("In-phase  (I)")
    ax.set_ylabel("Quadrature  (Q)")
    ax.set_aspect("equal")
    lim = 2.2
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[part2] constellation -> {path}")


# ---------- 2c. BER vs Eb/N0  (simulated vs theory) -------------------
def figure_ber_curve(png_path, svg_path, n_bits=1_000_000):
    ebn0_db = np.arange(0, 11)               # 0 .. 10 dB
    rng = np.random.default_rng(2024)

    sim_ber = np.full(ebn0_db.size, np.nan)
    n_errors = np.zeros(ebn0_db.size, dtype=int)
    for i, snr in enumerate(ebn0_db):
        bits = rng.integers(0, 2, n_bits)
        sym = bpsk_modulate(bits)
        r = awgn(sym, snr, rng)
        bhat = demodulate(r)
        err = int(np.sum(bhat != bits))
        n_errors[i] = err
        if err > 0:
            sim_ber[i] = err / n_bits

    g = 10.0 ** (ebn0_db / 10.0)
    theory_ber = 0.5 * erfc(np.sqrt(g))

    # console table (so the numbers can be reported / put in the write-up)
    print("\n  Eb/N0(dB) |   sim BER   |  theory BER |  errors / N")
    print("  ----------+-------------+-------------+-------------")
    for i, snr in enumerate(ebn0_db):
        sval = f"{sim_ber[i]:.3e}" if not np.isnan(sim_ber[i]) else "  0 (none) "
        print(f"     {snr:4.0f}  | {sval:>11} | {theory_ber[i]:.3e} | {n_errors[i]:>6d}/{n_bits}")

    fig, ax = plt.subplots(figsize=(9, 6.2))
    ax.semilogy(ebn0_db, theory_ber, "-", color=C_THEORY, linewidth=2.2,
                label=r"Theory:  $P_b = \frac{1}{2}\,\mathrm{erfc}(\sqrt{E_b/N_0})$")
    mask = ~np.isnan(sim_ber)
    ax.semilogy(ebn0_db[mask], sim_ber[mask], "o", color=C_BITS,
                markersize=8, markeredgecolor="white", markeredgewidth=1.0,
                label=f"Simulation  ({n_bits:,} bits / point)")
    ax.set_title("BPSK Bit-Error Rate over an AWGN Channel")
    ax.set_xlabel("$E_b/N_0$  (dB)")
    ax.set_ylabel("Bit Error Rate (BER)")
    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(1e-6, 1)
    ax.grid(True, which="both", color="#E0E0E0", linewidth=0.7)
    ax.grid(True, which="major", color="#BDBDBD", linewidth=0.9)
    ax.legend(loc="lower left", fontsize=10)
    fig.tight_layout()
    fig.savefig(png_path, dpi=150, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\n[part2] BER curve -> {png_path} , {svg_path}")


# ======================================================================
if __name__ == "__main__":
    print("=" * 64)
    print(" BPSK communication-system: diagram + signal-flow analysis")
    print("=" * 64)

    # Part 1
    draw_block_diagram(f"{OUT}/comm_system_block_diagram.png",
                       f"{OUT}/comm_system_block_diagram.svg")

    # Part 2
    figure_signal_flow(f"{OUT}/bpsk_signal_flow.png")
    figure_constellation(f"{OUT}/bpsk_constellation.png", ebn0_db=8.0)
    figure_ber_curve(f"{OUT}/bpsk_ber_curve.png",
                     f"{OUT}/bpsk_ber_curve.svg")

    print("\nDone. All files written to", OUT)

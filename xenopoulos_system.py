"""
XENOPOULOS GENETIC-HISTORICAL LOGIC SYSTEM (XEPTQLRI)
Complete Implementation v2.0 with Paradoxical Transcendence Detection

Founder and Theorist: EPAMEINONDAS XENOPOULOS
Source: "Epistemology of Logic: Logic–Dialectic or Theory of Knowledge" (2024)
GitHub: https://github.com/kxenopoulou/epistemology-of-logic
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
import json
import pandas as pd
import matplotlib
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from scipy import stats
import sys
from datetime import datetime
import hashlib
import traceback

warnings.filterwarnings('ignore')

# Settings for Unicode and display
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['figure.dpi'] = 100
sns.set_style("whitegrid")

print("="*80)
print("XENOPOULOS GENETIC-HISTORICAL LOGIC SYSTEM v2.0")
print("Enhanced with Paradoxical Transcendence Detection")
print("="*80)

class XenopoulosGeneticHistoricalSystem:
    """
    Complete Implementation of Xenopoulos' Genetic-Historical Logic System
    with the XEPTQLRI (Xenopoulos Pre‑Transitional Qualitative Leap Risk Index)
    
    Founder: Epameinondas Xenopoulos
    Based on: "Epistemology of Logic: Logic–Dialectic or Theory of Knowledge" (2024)
    """
    
    def __init__(self, initial_state_A=0.3, historical_horizon=200, 
                 aufhebung_threshold=0.85, volatility_factor=0.03,
                 system_name="Default System", seed=None):
        """
        Initialize the Xenopoulos Genetic-Historical Logic System.
        
        Parameters:
        -----------
        initial_state_A : float
            Initial value of system state A (0-1 normalized)
        historical_horizon : int
            Number of time steps for simulation/analysis
        aufhebung_threshold : float
            Critical tension threshold for qualitative transition (⤊ operator)
        volatility_factor : float
            Stochastic volatility factor of the dialectical process
        system_name : str
            Name identifier for the system
        seed : int, optional
            Random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
        
        self.A = np.clip(initial_state_A, 0, 1)
        self.horizon = historical_horizon
        self.aufhebung_threshold = aufhebung_threshold
        self.volatility = volatility_factor
        self.system_name = system_name
        self.creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.system_id = hashlib.md5(f"{system_name}{initial_state_A}{historical_horizon}".encode()).hexdigest()[:8]
        
        # Initial dialectical negation ¬ᴰA
        self.anti_A = self._enhanced_dialectical_negation(self.A)
        
        # Historical tracking
        self.history_A = []
        self.history_anti_A = []
        self.history_tension = []
        self.history_XEPTQLRI = []
        self.history_true_XEPTQLRI = []
        self.history_stages = []
        self.history_true_stages = []
        self.history_paradox_scores = []
        self.risk_events = []
        self.paradox_events = []
        self.phase_history = []
        
        # Enhanced dialectical stages with paradox detection
        self.stages = {
            0: "τ₀: Coherence",
            1: "τ₁: First Anomaly", 
            2: "τ₂: Anomaly Repetition",
            3: "τ₃: Meaning Incompatibility",
            4: "τ₄: System Saturation",
            5: "τ₅: Qualitative Leap (⤊)",
            6: "τ₆: Paradoxical Transcendence (⟡)",
            7: "τ₇: False Stability",
            8: "τ₈: Permanent Dialectics",
            9: "τ₉: Meta-Transcendence"
        }
        
        # Enhanced phase definitions
        self.phases = {
            0: "Stability Phase",
            1: "Anomaly Phase", 
            2: "Contradiction Phase",
            3: "Crisis Phase",
            4: "Transition Phase",
            5: "Paradox Phase",
            6: "Meta-Stability Phase"
        }
        
        # System metadata
        self.metadata = {
            'system_id': self.system_id,
            'creation_time': self.creation_time,
            'initial_state': float(self.A),
            'horizon': self.horizon,
            'aufhebung_threshold': self.aufhebung_threshold,
            'volatility': self.volatility,
            'stage_count': len(self.stages)
        }
        
        print(f"⚡ ENHANCED XENOPOULOS SYSTEM INITIALIZED")
        print(f"   System ID: {self.system_id}")
        print(f"   Name: {self.system_name}")
        print(f"   Initial State (A): {self.A:.3f}")
        print(f"   Dialectical Negation (¬ᴰA): {self.anti_A:.3f}")
        print(f"   Historical Horizon: {self.horizon} steps")
        print(f"   Aufhebung Threshold: {self.aufhebung_threshold}")
        print(f"   Enhanced Stages: {len(self.stages)} stages")
    
    # ============================================================================
    # CORE DIALECTICAL OPERATORS
    # ============================================================================
    
    def _enhanced_dialectical_negation(self, state):
        """
        Enhanced ¬ᴰ operator with historical memory and paradox awareness.
        
        According to Xenopoulos: "Not 'not-A' but 'the internal opposition that preserves A'"
        """
        preservation_factor = 0.8 + 0.2 * np.random.rand()
        
        historical_effect = 0.0
        if len(self.history_A) > 0:
            recent_mean = np.mean(self.history_A[-10:] if len(self.history_A) >= 10 else self.history_A)
            historical_effect = 0.1 * np.tanh(recent_mean)
        
        paradox_feedback = 0.0
        if len(self.history_paradox_scores) > 0 and np.mean(self.history_paradox_scores[-5:]) > 0.7:
            paradox_feedback = 0.05 * np.random.randn()
        
        enhanced_negation = -state * preservation_factor * (1 + historical_effect + paradox_feedback)
        stochastic_component = self.volatility * 0.1 * np.random.randn()
        
        return enhanced_negation + stochastic_component
    
    def _dialectical_conjunction_intensity(self, state, anti_state):
        """
        Calculate intensity of (A ∧ᴰ ¬ᴰA) with paradox awareness.
        
        According to Xenopoulos: "Creates logically valid contradictions"
        """
        raw_intensity = np.abs(state * anti_state)
        
        if abs(state) > 0.8 and abs(anti_state) > 0.8:
            complexity_factor = 1.5 + self.volatility * np.random.randn()
        else:
            complexity_factor = 1 + self.volatility * np.random.randn()
        
        intensity = np.clip(raw_intensity * complexity_factor, 0, 1)
        return intensity
    
    def _calculate_paradox_score(self, state, anti_state, tension):
        """
        Calculate paradox score for enhanced detection.
        """
        extremity_score = min(abs(state), abs(anti_state))
        symmetry_score = 1 - abs(abs(state) - abs(anti_state))
        
        if extremity_score > 0.7 and tension < 0.3:
            tension_paradox = 0.5
        else:
            tension_paradox = 0
        
        persistence_score = 0
        if len(self.history_A) > 10:
            recent_states = self.history_A[-10:]
            recent_anti = self.history_anti_A[-10:]
            if np.mean([abs(s) for s in recent_states]) > 0.7 and np.mean([abs(a) for a in recent_anti]) > 0.7:
                persistence_score = 0.3
        
        paradox_score = (extremity_score * 0.4 + 
                        symmetry_score * 0.3 + 
                        tension_paradox * 0.2 + 
                        persistence_score * 0.1)
        
        return np.clip(paradox_score, 0, 1)
    
    def _enhanced_stage_classification(self, tension_score, current_A, current_anti_A, paradox_score):
        """
        Enhanced stage classification with paradox detection.
        """
        # Paradox Detection First
        if abs(current_A) > 0.8 and abs(current_anti_A) > 0.8:
            if tension_score < 0.4:
                return 6, self.stages[6]  # τ₆: Paradoxical Transcendence
        
        if tension_score < 0.3:
            if abs(current_A) > 0.7 or abs(current_anti_A) > 0.7:
                return 7, self.stages[7]  # τ₇: False Stability
        
        if len(self.history_stages) > 20:
            recent_stages = self.history_stages[-20:]
            if len(set(recent_stages)) >= 4 and np.std(recent_stages) > 1.5:
                return 8, self.stages[8]  # τ₈: Permanent Dialectics
        
        if paradox_score > 0.8 and tension_score > 0.6:
            return 9, self.stages[9]  # τ₉: Meta-Transcendence
        
        # Original Stage Classification
        if tension_score < 0.15:
            return 0, self.stages[0]
        elif tension_score < 0.35:
            return 1, self.stages[1]
        elif tension_score < 0.55:
            return 2, self.stages[2]
        elif tension_score < 0.75:
            return 3, self.stages[3]
        elif tension_score < self.aufhebung_threshold:
            return 4, self.stages[4]
        else:
            return 5, self.stages[5]
    
    def _calculate_enhanced_XEPTQLRI(self, tension, historical_trend, current_A, current_anti_A, paradox_score):
        """
        Enhanced XEPTQLRI calculation with paradox awareness.
        """
        trend_factor = 1.0
        if historical_trend > 0.1:
            trend_factor = 1.5
        elif historical_trend > 0.3:
            trend_factor = 2.0
        
        paradox_factor = 1.0
        if paradox_score > 0.7:
            if tension < 0.3:
                paradox_factor = 1.8  # False Stability - HIGH RISK
            else:
                paradox_factor = 2.0  # Paradox with high tension
        
        extremity_multiplier = 1.0
        if abs(current_A) > 0.8 and abs(current_anti_A) > 0.8:
            extremity_multiplier = 1.5
        
        enhanced_XEPTQLRI = (tension * trend_factor * paradox_factor * extremity_multiplier) / self.aufhebung_threshold
        
        stochastic_factor = 1 + (self.volatility * 0.3 * np.random.randn())
        enhanced_XEPTQLRI = enhanced_XEPTQLRI * stochastic_factor
        
        if len(self.history_A) > 50:
            recent_extremity = np.mean([abs(x) > 0.8 for x in self.history_A[-50:]])
            if recent_extremity > 0.7:
                enhanced_XEPTQLRI *= 1.3
        
        return np.clip(enhanced_XEPTQLRI, 0, 3.0)
    
    # ============================================================================
    # SIMULATION AND ANALYSIS
    # ============================================================================
    
    def simulate_enhanced_historical_process(self):
        """
        Simulate historical process with enhanced paradox detection.
        """
        print(f"\n🌌 SIMULATING {self.system_name.upper()} WITH PARADOX DETECTION...")
        print(f"   Enhanced stages: {len(self.stages)}")
        print(f"   System ID: {self.system_id}")
        
        current_A = self.A
        current_anti_A = self.anti_A
        
        # Enhanced phase boundaries
        phase_boundaries = [
            int(self.horizon * 0.2),
            int(self.horizon * 0.4),
            int(self.horizon * 0.6),
            int(self.horizon * 0.75),
            int(self.horizon * 0.85),
            int(self.horizon * 0.95),
            self.horizon
        ]
        
        for step in range(self.horizon):
            # Determine current phase
            current_phase = 0
            for p, boundary in enumerate(phase_boundaries):
                if step < boundary:
                    current_phase = p
                    break
            
            # Phase parameters
            phase_params = {
                0: {"pressure": 0.02, "volatility": 0.01},
                1: {"pressure": 0.05, "volatility": 0.03},
                2: {"pressure": 0.10, "volatility": 0.05},
                3: {"pressure": 0.15, "volatility": 0.08},
                4: {"pressure": 0.20, "volatility": 0.12},
                5: {"pressure": 0.25, "volatility": 0.15},
                6: {"pressure": 0.30, "volatility": 0.20}
            }
            
            params = phase_params[current_phase]
            
            # Update dialectical negation
            historical_factor = 1 + 0.003 * step
            current_anti_A = self._enhanced_dialectical_negation(current_A) * historical_factor
            
            # Calculate current tension
            current_tension = self._dialectical_conjunction_intensity(current_A, current_anti_A)
            
            # Apply dialectical pressure
            dialectical_pressure = current_tension * params["pressure"]
            
            # Add phase-specific patterns
            phase_pattern = {
                0: 0.01 * np.sin(step * 0.05),
                1: 0.02 * np.sin(step * 0.08),
                2: 0.03 * np.sin(step * 0.12),
                3: 0.04 * np.sin(step * 0.18),
                4: 0.05 * np.sin(step * 0.25),
                5: 0.06 * np.sin(step * 0.35),
                6: 0.03 * np.sin(step * 0.10)
            }
            historical_trend = phase_pattern[current_phase]
            
            # Add systemic noise
            systemic_noise = params["volatility"] * np.random.randn()
            
            # Update A
            current_A = current_A + dialectical_pressure + historical_trend + systemic_noise
            current_A = np.clip(current_A, -1.2, 1.2)
            
            # Calculate historical trend for XEPTQLRI
            if step > 10:
                recent_trend = np.polyfit(range(10), self.history_tension[-10:], 1)[0] if len(self.history_tension) >= 10 else 0
            else:
                recent_trend = 0
            
            # Calculate paradox score
            paradox_score = self._calculate_paradox_score(current_A, current_anti_A, current_tension)
            
            # Calculate enhanced XEPTQLRI
            enhanced_XEPTQLRI = self._calculate_enhanced_XEPTQLRI(
                current_tension, recent_trend, current_A, current_anti_A, paradox_score
            )
            
            # Enhanced stage classification
            stage_idx, stage_name = self._enhanced_stage_classification(
                current_tension, current_A, current_anti_A, paradox_score
            )
            
            # Detect paradox events
            self._detect_paradox_events(step, current_A, current_anti_A, paradox_score, stage_idx)
            
            # Store enhanced history
            self.history_A.append(current_A)
            self.history_anti_A.append(current_anti_A)
            self.history_tension.append(current_tension)
            self.history_XEPTQLRI.append(enhanced_XEPTQLRI)
            self.history_true_XEPTQLRI.append(enhanced_XEPTQLRI)
            self.history_stages.append(stage_idx)
            self.history_true_stages.append(stage_idx)
            self.history_paradox_scores.append(paradox_score)
            self.phase_history.append(current_phase)
            
            # Detect risk events
            if enhanced_XEPTQLRI > 0.7:
                risk_level = "CRITICAL" if enhanced_XEPTQLRI > 1.0 else "HIGH"
                self.risk_events.append({
                    'step': step,
                    'XEPTQLRI': enhanced_XEPTQLRI,
                    'true_XEPTQLRI': enhanced_XEPTQLRI,
                    'tension': current_tension,
                    'stage': stage_name,
                    'risk': risk_level,
                    'phase': self.phases[current_phase],
                    'paradox_score': paradox_score
                })
            
            # Progress indicator
            if step % 50 == 0 and step > 0:
                sys.stdout.write(f"\r   Progress: {step}/{self.horizon} steps | "
                               f"Current Stage: {stage_name[:20]} | "
                               f"Paradox Score: {paradox_score:.2f}")
                sys.stdout.flush()
        
        print(f"\r   ✅ Enhanced simulation completed: {self.horizon} steps")
        print(f"   ⚡ Risk events detected: {len(self.risk_events)}")
        print(f"   🔮 Paradox events detected: {len(self.paradox_events)}")
        print(f"   🎭 Final Stage: {self.stages[self.history_stages[-1]]}")
        print(f"   📊 Final Paradox Score: {self.history_paradox_scores[-1]:.3f}")
        
        return self
    
    def _detect_paradox_events(self, step, current_A, current_anti_A, paradox_score, stage_idx):
        """
        Detect and record special paradox events.
        """
        if abs(current_A) > 0.85 and abs(current_anti_A) > 0.85:
            self.paradox_events.append({
                'step': step,
                'type': 'SIMULTANEOUS_EXTREMITY',
                'A_value': float(current_A),
                'anti_A_value': float(current_anti_A),
                'paradox_score': float(paradox_score),
                'stage': self.stages[stage_idx],
                'description': 'Both A and ¬A at extreme values simultaneously'
            })
        
        if stage_idx == 7:
            self.paradox_events.append({
                'step': step,
                'type': 'FALSE_STABILITY',
                'A_value': float(current_A),
                'anti_A_value': float(current_anti_A),
                'paradox_score': float(paradox_score),
                'stage': self.stages[stage_idx],
                'description': 'System appears stable but is at extreme values'
            })
        
        if paradox_score > 0.9:
            self.paradox_events.append({
                'step': step,
                'type': 'META_PARADOX',
                'A_value': float(current_A),
                'anti_A_value': float(current_anti_A),
                'paradox_score': float(paradox_score),
                'stage': self.stages[stage_idx],
                'description': 'Extreme paradox score detected'
            })
    
    def _calculate_stability_deception_index(self):
        """
        Calculate how deceptive the apparent stability is.
        """
        if len(self.history_XEPTQLRI) < 50:
            return 0.0
        
        recent_risk = np.mean(self.history_XEPTQLRI[-50:])
        recent_A_abs = np.mean([abs(x) for x in self.history_A[-50:]])
        recent_anti_abs = np.mean([abs(x) for x in self.history_anti_A[-50:]])
        
        if recent_risk < 0.5:
            if recent_A_abs > 0.7 or recent_anti_abs > 0.7:
                deception = min(1.0, (recent_A_abs + recent_anti_abs) / 2)
            else:
                deception = 0.0
        else:
            deception = 0.0
        
        return float(deception)
    
    # ============================================================================
    # ANALYSIS AND REPORTING
    # ============================================================================
    
    def enhanced_analysis_report(self):
        """
        Generate comprehensive enhanced analysis report.
        """
        if not self.history_XEPTQLRI:
            self.simulate_enhanced_historical_process()
        
        XEPTQLRI_array = np.array(self.history_XEPTQLRI)
        paradox_array = np.array(self.history_paradox_scores)
        
        # Enhanced metrics
        report = {
            'system_info': {
                'name': self.system_name,
                'id': self.system_id,
                'creation_time': self.creation_time,
                'total_steps': len(self.history_A)
            },
            'metrics': {
                'mean_XEPTQLRI': float(np.mean(XEPTQLRI_array)),
                'max_XEPTQLRI': float(np.max(XEPTQLRI_array)),
                'min_XEPTQLRI': float(np.min(XEPTQLRI_array)),
                'final_XEPTQLRI': float(XEPTQLRI_array[-1]),
                'std_XEPTQLRI': float(np.std(XEPTQLRI_array)),
                'mean_tension': float(np.mean(self.history_tension)),
                'max_tension': float(np.max(self.history_tension)),
                'mean_paradox_score': float(np.mean(paradox_array)),
                'max_paradox_score': float(np.max(paradox_array)),
                'stability_deception': float(self._calculate_stability_deception_index()),
                'permanent_transcendence_score': float(np.mean([abs(x) > 0.8 for x in self.history_A])),
                'simultaneous_extremity_score': float(np.mean([abs(a) > 0.8 and abs(b) > 0.8 
                                                              for a, b in zip(self.history_A, self.history_anti_A)]))
            },
            'current_state': {
                'stage': self.stages[self.history_stages[-1]],
                'stage_index': int(self.history_stages[-1]),
                'A_value': float(self.history_A[-1]),
                'anti_A_value': float(self.history_anti_A[-1]),
                'paradox_score': float(self.history_paradox_scores[-1]),
                'phase': self.phases[self.phase_history[-1]]
            },
            'distribution': {
                'stages': {},
                'phases': {},
                'risk_levels': {
                    'low': np.sum(XEPTQLRI_array < 0.5),
                    'medium': np.sum((XEPTQLRI_array >= 0.5) & (XEPTQLRI_array < 1.0)),
                    'high': np.sum((XEPTQLRI_array >= 1.0) & (XEPTQLRI_array < 2.0)),
                    'extreme': np.sum(XEPTQLRI_array >= 2.0)
                }
            },
            'paradox_analysis': {
                'total_paradox_events': len(self.paradox_events),
                'simultaneous_extremity_events': len([e for e in self.paradox_events if e['type'] == 'SIMULTANEOUS_EXTREMITY']),
                'false_stability_events': len([e for e in self.paradox_events if e['type'] == 'FALSE_STABILITY']),
                'meta_paradox_events': len([e for e in self.paradox_events if e['type'] == 'META_PARADOX']),
                'paradox_persistence': float(np.mean(paradox_array > 0.7))
            }
        }
        
        # Stage distribution
        for idx, name in self.stages.items():
            count = np.sum(np.array(self.history_stages) == idx)
            report['distribution']['stages'][name] = int(count)
        
        # Phase distribution
        for idx, name in self.phases.items():
            count = np.sum(np.array(self.phase_history) == idx)
            report['distribution']['phases'][name] = int(count)
        
        # Determine true system state
        true_state = self._determine_true_system_state()
        report['true_system_state'] = true_state
        
        # Generate enhanced recommendations
        recommendations = self._generate_enhanced_recommendations(report)
        report['recommendations'] = recommendations
        
        return report
    
    def _determine_true_system_state(self):
        """
        Determine the true state of the system beyond apparent stability.
        """
        if len(self.history_A) < 100:
            return "INSUFFICIENT_DATA"
        
        recent_A = self.history_A[-100:]
        recent_anti = self.history_anti_A[-100:]
        recent_paradox = self.history_paradox_scores[-100:]
        recent_stages = self.history_stages[-100:]
        
        time_at_extremes = np.mean([abs(x) > 0.8 for x in recent_A])
        simultaneous_extremes = np.mean([abs(a) > 0.8 and abs(b) > 0.8 
                                        for a, b in zip(recent_A, recent_anti)])
        paradox_persistence = np.mean([p > 0.7 for p in recent_paradox])
        stage_variability = np.std(recent_stages)
        
        # Decision tree
        if paradox_persistence > 0.6:
            if time_at_extremes > 0.7:
                return "PERMANENT_PARADOXICAL_TRANSCENDENCE"
            else:
                return "INTERMITTENT_PARADOXICAL_STATE"
        
        elif simultaneous_extremes > 0.5:
            return "SIMULTANEOUS_EXTREMITY_REGIME"
        
        elif time_at_extremes > 0.8:
            return "PERMANENT_TRANSCENDENCE"
        
        elif stage_variability > 2.0:
            return "CHAOTIC_DIALECTICS"
        
        elif np.mean(self.history_XEPTQLRI[-100:]) < 0.3:
            if time_at_extremes > 0.3:
                return "FALSE_STABILITY_REGIME"
            else:
                return "TRUE_STABILITY"
        
        else:
            return "DYNAMIC_EQUILIBRIUM"
    
    def _generate_enhanced_recommendations(self, report):
        """
        Generate enhanced recommendations based on true system state.
        """
        true_state = report['true_system_state']
        metrics = report['metrics']
        
        recommendations = []
        
        if "PARADOXICAL_TRANSCENDENCE" in true_state:
            recommendations.extend([
                "🚨 IMMEDIATE ATTENTION: System in paradoxical transcendence state",
                "Re-evaluate fundamental assumptions about system stability",
                "Implement paradoxical stability protocols",
                "Monitor for meta-paradox escalation",
                "Document all simultaneous extremity events"
            ])
        elif "FALSE_STABILITY" in true_state:
            recommendations.extend([
                "⚠️ CAUTION: System exhibiting false stability characteristics",
                "Apparent stability masks underlying extremity",
                "Increase monitoring frequency 2x",
                "Implement deception detection protocols",
                "Review historical patterns for similar episodes"
            ])
        elif "SIMULTANEOUS_EXTREMITY" in true_state:
            recommendations.extend([
                "⚡ WARNING: Simultaneous extremity regime detected",
                "Both A and ¬A operating at extreme values",
                "Prepare for potential phase transition",
                "Monitor paradox score closely",
                "Consider implementing paradox resolution protocols"
            ])
        elif metrics['max_XEPTQLRI'] > 2.0:
            recommendations.extend([
                "🔴 CRITICAL: Extreme XEPTQLRI values detected",
                "System approaching theoretical limits",
                "Implement emergency protocols",
                "Prepare for qualitative leap (⤊)",
                "Document all parameters for post-transition analysis"
            ])
        elif metrics['stability_deception'] > 0.5:
            recommendations.extend([
                "🎭 DECEPTION ALERT: High stability deception index",
                "System appears more stable than it actually is",
                "Implement truth-revealing protocols",
                "Cross-validate with alternative metrics",
                "Review with paradox-aware analysis"
            ])
        elif true_state == "TRUE_STABILITY":
            recommendations.extend([
                "✅ System operating in true stability regime",
                "Maintain current monitoring protocols",
                "Periodic paradox detection checks",
                "Document baseline for future comparisons"
            ])
        else:
            recommendations.extend([
                "📊 System in dynamic equilibrium",
                "Continue standard monitoring",
                "Watch for paradoxical developments",
                "Maintain paradox detection systems"
            ])
        
        if report['paradox_analysis']['total_paradox_events'] > 10:
            recommendations.append(f"🔮 High paradox event count: {report['paradox_analysis']['total_paradox_events']} events")
        
        if metrics['simultaneous_extremity_score'] > 0.3:
            recommendations.append(f"⚖️ Simultaneous extremity observed {metrics['simultaneous_extremity_score']*100:.1f}% of time")
        
        return recommendations
    
    # ============================================================================
    # VISUALIZATION
    # ============================================================================
    
    def create_paradox_detection_dashboard(self):
        """
        Create comprehensive dashboard focusing on paradox detection.
        """
        if not self.history_XEPTQLRI:
            self.simulate_enhanced_historical_process()
        
        fig = plt.figure(figsize=(20, 24))
        fig.suptitle(f'PARADOX DETECTION DASHBOARD: {self.system_name}\n'
                    f'Enhanced Xenopoulos Genetic-Historical Logic System v2.0\n'
                    f'System ID: {self.system_id}', 
                    fontsize=18, fontweight='bold', y=0.995)
        
        gs = fig.add_gridspec(6, 4, hspace=0.25, wspace=0.25, height_ratios=[1.2, 1, 1, 1, 1, 1.5])
        
        # 1. Main Paradox Visualization
        ax1 = fig.add_subplot(gs[0, :])
        
        phase_colors = ['#e6f3ff', '#fff0e6', '#ffe6e6', '#ffcccc', '#ffb3b3', '#ff9999', '#ff6666']
        for phase in range(7):
            indices = np.where(np.array(self.phase_history) == phase)[0]
            if len(indices) > 0:
                for i in range(0, len(indices), 2):
                    if i+1 < len(indices):
                        ax1.axvspan(indices[i], indices[i+1], 
                                   alpha=0.15, color=phase_colors[phase])
        
        ax1.plot(self.history_A, 'b-', linewidth=2.5, alpha=0.9, 
                label='A (System State)')
        ax1.plot(self.history_anti_A, 'r-', linewidth=2.5, alpha=0.7, 
                label='¬ᴰA (Dialectical Negation)', linestyle='--')
        
        extreme_indices = [i for i, (a, anti) in enumerate(zip(self.history_A, self.history_anti_A)) 
                          if abs(a) > 0.8 or abs(anti) > 0.8]
        if extreme_indices:
            ax1.scatter(extreme_indices, [self.history_A[i] for i in extreme_indices], 
                       color='red', s=10, alpha=0.5, label='Extreme A values')
            ax1.scatter(extreme_indices, [self.history_anti_A[i] for i in extreme_indices], 
                       color='darkred', s=10, alpha=0.5, label='Extreme ¬A values')
        
        ax1.set_title('SYSTEM STATE EVOLUTION with Paradox Detection', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Historical Step', fontsize=11)
        ax1.set_ylabel('State Value', fontsize=11)
        ax1.axhline(y=0.8, color='orange', linestyle=':', alpha=0.5, label='Extreme Threshold (+0.8)')
        ax1.axhline(y=-0.8, color='orange', linestyle=':', alpha=0.5, label='Extreme Threshold (-0.8)')
        ax1.grid(True, alpha=0.2)
        ax1.legend(loc='upper right', fontsize=9, ncol=3)
        
        # 2. Paradox Score Timeline
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(self.history_paradox_scores, 'purple', linewidth=2, alpha=0.8)
        ax2.fill_between(range(len(self.history_paradox_scores)), 
                        self.history_paradox_scores, alpha=0.3, color='purple')
        ax2.axhline(y=0.7, color='red', linestyle='--', alpha=0.7, label='Paradox Threshold (0.7)')
        ax2.set_title('Paradox Score Timeline', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Paradox Score')
        ax2.set_ylim(0, 1.1)
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.2)
        
        # 3. Enhanced XEPTQLRI
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(self.history_XEPTQLRI, 'darkgreen', linewidth=2, alpha=0.8)
        ax3.axhline(y=1.0, color='darkred', linestyle='-', alpha=0.7, label='Critical (1.0)')
        ax3.axhline(y=0.7, color='orange', linestyle='--', alpha=0.7, label='Warning (0.7)')
        ax3.axhline(y=2.0, color='black', linestyle=':', alpha=0.7, label='Extreme (2.0)')
        ax3.set_title('Enhanced XEPTQLRI', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Step')
        ax3.set_ylabel('XEPTQLRI')
        ax3.legend(loc='upper left')
        ax3.grid(True, alpha=0.2)
        
        # 4. Stage Distribution
        ax4 = fig.add_subplot(gs[1, 2])
        stage_counts = [np.sum(np.array(self.history_stages) == i) for i in range(10)]
        colors = ['#2E8B57', '#FFD700', '#FF8C00', '#DC143C', '#8A2BE2', 
                 '#000000', '#FF00FF', '#00FFFF', '#FF1493', '#9400D3']
        bars = ax4.bar(range(10), stage_counts, color=colors, alpha=0.8)
        ax4.set_title('Enhanced Stage Distribution', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Stage')
        ax4.set_ylabel('Count')
        ax4.set_xticks(range(10))
        ax4.set_xticklabels([f'τ{i}' for i in range(10)], rotation=45, fontsize=9)
        
        for bar, count in zip(bars, stage_counts):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom', fontsize=8)
        
        # 5. Phase Space
        ax5 = fig.add_subplot(gs[1, 3])
        scatter = ax5.scatter(self.history_A, self.history_anti_A, 
                             c=self.history_paradox_scores, cmap='RdYlBu_r',
                             s=20, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        ax5.add_patch(Rectangle((0.8, 0.8), 0.4, 0.4, alpha=0.1, color='red', 
                               label='Paradox Zone I (+,+)'))
        ax5.add_patch(Rectangle((-1.2, -1.2), 0.4, 0.4, alpha=0.1, color='red',
                               label='Paradox Zone II (-,-)'))
        
        ax5.set_title('Phase Space: A vs ¬A with Paradox Zones', fontsize=12, fontweight='bold')
        ax5.set_xlabel('A Value')
        ax5.set_ylabel('¬A Value')
        ax5.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax5.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        ax5.set_xlim(-1.2, 1.2)
        ax5.set_ylim(-1.2, 1.2)
        ax5.grid(True, alpha=0.2)
        plt.colorbar(scatter, ax=ax5, label='Paradox Score')
        
        # 6. Tension vs Paradox Score
        ax6 = fig.add_subplot(gs[2, 0])
        scatter = ax6.scatter(self.history_tension, self.history_paradox_scores,
                             c=self.history_stages, cmap='tab20', s=30, alpha=0.7)
        ax6.set_title('Tension vs Paradox Score', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Dialectical Tension')
        ax6.set_ylabel('Paradox Score')
        ax6.grid(True, alpha=0.2)
        plt.colorbar(scatter, ax=ax6, label='Stage')
        
        # 7. Moving Averages
        ax7 = fig.add_subplot(gs[2, 1])
        window = 20
        if len(self.history_A) > window:
            moving_avg_A = np.convolve(self.history_A, np.ones(window)/window, mode='valid')
            moving_avg_anti = np.convolve(self.history_anti_A, np.ones(window)/window, mode='valid')
            
            ax7.plot(range(window-1, len(self.history_A)), moving_avg_A, 
                    'b-', linewidth=2, alpha=0.8, label=f'A ({window}-step MA)')
            ax7.plot(range(window-1, len(self.history_anti_A)), moving_avg_anti,
                    'r-', linewidth=2, alpha=0.6, label=f'¬A ({window}-step MA)')
            ax7.set_title(f'{window}-Step Moving Averages', fontsize=12, fontweight='bold')
            ax7.set_xlabel('Step')
            ax7.set_ylabel('Moving Average')
            ax7.legend()
            ax7.grid(True, alpha=0.2)
        
        # 8. Extremity Analysis
        ax8 = fig.add_subplot(gs[2, 2])
        extremity_A = [abs(x) for x in self.history_A]
        extremity_anti = [abs(x) for x in self.history_anti_A]
        simultaneous_extremity = [1 if a > 0.8 and b > 0.8 else 0 
                                 for a, b in zip(extremity_A, extremity_anti)]
        
        ax8.plot(extremity_A, 'b-', alpha=0.6, label='|A|')
        ax8.plot(extremity_anti, 'r-', alpha=0.6, label='|¬A|')
        ax8.plot(simultaneous_extremity, 'purple', linewidth=2, alpha=0.8, label='Simultaneous Extremity')
        ax8.axhline(y=0.8, color='orange', linestyle='--', alpha=0.5, label='Extreme Threshold')
        ax8.set_title('Extremity Analysis', fontsize=12, fontweight='bold')
        ax8.set_xlabel('Step')
        ax8.set_ylabel('Absolute Value')
        ax8.legend(loc='upper right', fontsize=8)
        ax8.grid(True, alpha=0.2)
        
        # 9. Stage Transitions with Paradox Events
        ax9 = fig.add_subplot(gs[2, 3])
        
        stage_changes = np.diff(self.history_stages)
        change_points = np.where(stage_changes != 0)[0]
        
        if len(change_points) > 0:
            ax9.plot(change_points, [self.history_stages[i] for i in change_points], 
                    'bo-', alpha=0.7, markersize=6, label='Stage Transitions')
        
        if self.paradox_events:
            for event in self.paradox_events:
                color = {'SIMULTANEOUS_EXTREMITY': 'red', 
                        'FALSE_STABILITY': 'orange', 
                        'META_PARADOX': 'purple'}.get(event['type'], 'black')
                ax9.scatter(event['step'], self.history_stages[event['step']], 
                          color=color, s=50, alpha=0.8)
        
        ax9.set_title('Stage Transitions with Paradox Events', fontsize=12, fontweight='bold')
        ax9.set_xlabel('Step')
        ax9.set_ylabel('Stage')
        ax9.set_yticks(range(10))
        ax9.set_yticklabels([f'τ{i}' for i in range(10)])
        ax9.grid(True, alpha=0.2)
        
        # 10. XEPTQLRI Distribution
        ax10 = fig.add_subplot(gs[3, 0])
        bins = np.linspace(0, max(self.history_XEPTQLRI) + 0.1, 30)
        ax10.hist(self.history_XEPTQLRI, bins=bins, color='green', alpha=0.7, edgecolor='black')
        ax10.axvline(x=1.0, color='red', linestyle='-', linewidth=2, label='Critical')
        ax10.axvline(x=0.7, color='orange', linestyle='--', linewidth=2, label='Warning')
        ax10.axvline(x=2.0, color='black', linestyle=':', linewidth=2, label='Extreme')
        ax10.set_title('XEPTQLRI Distribution', fontsize=12, fontweight='bold')
        ax10.set_xlabel('XEPTQLRI Value')
        ax10.set_ylabel('Frequency')
        ax10.legend()
        
        # 11. Paradox Event Timeline
        ax11 = fig.add_subplot(gs[3, 1])
        if self.paradox_events:
            for event in self.paradox_events:
                color = {'SIMULTANEOUS_EXTREMITY': 'red', 
                        'FALSE_STABILITY': 'orange', 
                        'META_PARADOX': 'purple'}.get(event['type'], 'gray')
                ax11.scatter(event['step'], 1, color=color, s=100, alpha=0.7)
            ax11.set_title('Paradox Event Timeline', fontsize=12, fontweight='bold')
            ax11.set_xlabel('Step')
            ax11.set_yticks([])
        else:
            ax11.text(0.5, 0.5, 'No Paradox Events Detected', 
                     ha='center', va='center', fontsize=14, transform=ax11.transAxes)
            ax11.set_title('Paradox Event Timeline', fontsize=12, fontweight='bold')
        
        # 12. Phase Distribution
        ax12 = fig.add_subplot(gs[3, 2])
        phase_counts = [np.sum(np.array(self.phase_history) == i) for i in range(7)]
        phase_labels = [f'P{i}' for i in range(7)]
        colors = ['#e6f3ff', '#fff0e6', '#ffe6e6', '#ffcccc', '#ffb3b3', '#ff9999', '#ff6666']
        
        wedges, texts, autotexts = ax12.pie(phase_counts, labels=phase_labels,
                                           autopct='%1.1f%%', colors=colors,
                                           startangle=90)
        ax12.set_title('Phase Distribution', fontsize=12, fontweight='bold')
        
        # 13. Correlation Matrix
        ax13 = fig.add_subplot(gs[3, 3])
        
        data_for_corr = np.array([
            self.history_A,
            self.history_anti_A,
            self.history_tension,
            self.history_XEPTQLRI,
            self.history_paradox_scores,
            self.history_stages
        ]).T
        
        corr_matrix = np.corrcoef(data_for_corr.T)
        
        im = ax13.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
        ax13.set_title('Correlation Matrix', fontsize=12, fontweight='bold')
        ax13.set_xticks(range(6))
        ax13.set_yticks(range(6))
        ax13.set_xticklabels(['A', '¬A', 'Tension', 'XEPTQLRI', 'Paradox', 'Stage'], 
                            rotation=45, fontsize=9)
        ax13.set_yticklabels(['A', '¬A', 'Tension', 'XEPTQLRI', 'Paradox', 'Stage'], 
                            fontsize=9)
        
        for i in range(6):
            for j in range(6):
                ax13.text(j, i, f'{corr_matrix[i, j]:.2f}', 
                         ha='center', va='center', color='white' if abs(corr_matrix[i, j]) > 0.5 else 'black',
                         fontsize=8)
        
        plt.colorbar(im, ax=ax13)
        
        # 14. Detailed Analysis Report
        ax14 = fig.add_subplot(gs[4:, :])
        ax14.axis('off')
        
        report = self.enhanced_analysis_report()
        true_state = report['true_system_state']
        
        if "PARADOXICAL" in true_state or "FALSE_STABILITY" in true_state:
            box_color = '#FFCCCC'
            border_color = 'red'
        elif "EXTREMITY" in true_state or "CRITICAL" in true_state:
            box_color = '#FFE5CC'
            border_color = 'orange'
        elif "TRUE_STABILITY" in true_state:
            box_color = '#CCFFCC'
            border_color = 'green'
        else:
            box_color = '#E6F3FF'
            border_color = 'blue'
        
        report_text = (
            f"{'='*70}\n"
            f"ENHANCED XEPTQLRI ANALYSIS REPORT - PARADOX DETECTION EDITION\n"
            f"{'='*70}\n\n"
            f"SYSTEM INFORMATION:\n"
            f"• Name: {report['system_info']['name']}\n"
            f"• ID: {report['system_info']['id']}\n"
            f"• Total Steps: {report['system_info']['total_steps']}\n"
            f"• Creation Time: {report['system_info']['creation_time']}\n\n"
            
            f"CURRENT STATE ANALYSIS:\n"
            f"• Current Stage: {report['current_state']['stage']}\n"
            f"• Current Phase: {report['current_state']['phase']}\n"
            f"• Current A: {report['current_state']['A_value']:.3f}\n"
            f"• Current ¬A: {report['current_state']['anti_A_value']:.3f}\n"
            f"• Current Paradox Score: {report['current_state']['paradox_score']:.3f}\n\n"
            
            f"TRUE SYSTEM STATE DIAGNOSIS:\n"
            f"• Apparent Stability: {'Stable' if report['metrics']['mean_XEPTQLRI'] < 0.5 else 'Unstable'}\n"
            f"• True System State: {true_state}\n"
            f"• Stability Deception Index: {report['metrics']['stability_deception']:.3f}\n"
            f"• Permanent Transcendence Score: {report['metrics']['permanent_transcendence_score']:.3f}\n"
            f"• Simultaneous Extremity Score: {report['metrics']['simultaneous_extremity_score']:.3f}\n\n"
            
            f"PARADOX ANALYSIS:\n"
            f"• Total Paradox Events: {report['paradox_analysis']['total_paradox_events']}\n"
            f"• Simultaneous Extremity Events: {report['paradox_analysis']['simultaneous_extremity_events']}\n"
            f"• False Stability Events: {report['paradox_analysis']['false_stability_events']}\n"
            f"• Meta-Paradox Events: {report['paradox_analysis']['meta_paradox_events']}\n"
            f"• Paradox Persistence: {report['paradox_analysis']['paradox_persistence']:.1%}\n\n"
            
            f"XEPTQLRI METRICS:\n"
            f"• Mean: {report['metrics']['mean_XEPTQLRI']:.3f}\n"
            f"• Max: {report['metrics']['max_XEPTQLRI']:.3f}\n"
            f"• Min: {report['metrics']['min_XEPTQLRI']:.3f}\n"
            f"• Std Dev: {report['metrics']['std_XEPTQLRI']:.3f}\n"
            f"• Final: {report['metrics']['final_XEPTQLRI']:.3f}\n\n"
            
            f"RISK DISTRIBUTION:\n"
            f"• Low Risk (XEPTQLRI < 0.5): {report['distribution']['risk_levels']['low']} steps\n"
            f"• Medium Risk (0.5 ≤ XEPTQLRI < 1.0): {report['distribution']['risk_levels']['medium']} steps\n"
            f"• High Risk (1.0 ≤ XEPTQLRI < 2.0): {report['distribution']['risk_levels']['high']} steps\n"
            f"• Extreme Risk (XEPTQLRI ≥ 2.0): {report['distribution']['risk_levels']['extreme']} steps\n\n"
            
            f"RECOMMENDATIONS:\n"
        )
        
        for i, rec in enumerate(report['recommendations'], 1):
            report_text += f"{i}. {rec}\n"
        
        ax14.text(0.02, 0.98, report_text, fontsize=9, family='monospace',
                 verticalalignment='top', transform=ax14.transAxes,
                 bbox=dict(boxstyle='round', facecolor=box_color, alpha=0.9,
                          edgecolor=border_color, linewidth=3))
        
        plt.tight_layout()
        return fig
    
    # ============================================================================
    # EXPORT FUNCTIONALITY
    # ============================================================================
    
    def export_comprehensive_analysis(self):
        """
        Export comprehensive analysis with multiple formats.
        """
        if not self.history_XEPTQLRI:
            self.simulate_enhanced_historical_process()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"xenopoulos_v2_{self.system_id}_{timestamp}"
        
        exports = {}
        
        # 1. Export JSON report
        report = self.enhanced_analysis_report()
        json_file = f"{base_filename}_report.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        exports['json_report'] = json_file
        
        # 2. Export CSV data
        df = pd.DataFrame({
            'step': range(len(self.history_A)),
            'A': self.history_A,
            'anti_A': self.history_anti_A,
            'tension': self.history_tension,
            'XEPTQLRI': self.history_XEPTQLRI,
            'paradox_score': self.history_paradox_scores,
            'stage': self.history_stages,
            'stage_name': [self.stages[s] for s in self.history_stages],
            'phase': self.phase_history,
            'phase_name': [self.phases[p] for p in self.phase_history]
        })
        
        csv_file = f"{base_filename}_data.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8')
        exports['csv_data'] = csv_file
        
        # 3. Export dashboard visualization
        fig = self.create_paradox_detection_dashboard()
        dashboard_file = f"{base_filename}_dashboard.png"
        fig.savefig(dashboard_file, dpi=150, bbox_inches='tight', facecolor='white')
        exports['dashboard_png'] = dashboard_file
        plt.close(fig)
        
        # 4. Export summary report
        summary_file = f"{base_filename}_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"XENOPOULOS SYSTEM v2.0 - COMPREHENSIVE ANALYSIS SUMMARY\n")
            f.write("="*70 + "\n\n")
            f.write(f"System: {self.system_name}\n")
            f.write(f"ID: {self.system_id}\n")
            f.write(f"Analysis Time: {timestamp}\n\n")
            f.write(f"TRUE SYSTEM STATE: {report['true_system_state']}\n\n")
            f.write("KEY METRICS:\n")
            f.write(f"  Max XEPTQLRI: {report['metrics']['max_XEPTQLRI']:.3f}\n")
            f.write(f"  Mean Paradox Score: {report['metrics']['mean_paradox_score']:.3f}\n")
            f.write(f"  Stability Deception: {report['metrics']['stability_deception']:.3f}\n")
            f.write(f"  Paradox Events: {report['paradox_analysis']['total_paradox_events']}\n\n")
        
        exports['summary_txt'] = summary_file
        
        print(f"\n✅ COMPREHENSIVE ANALYSIS EXPORTED:")
        for key, filepath in exports.items():
            print(f"   📁 {key}: {filepath}")
        
        return exports
    
    def _export_individual_visualizations(self, base_filename):
        """Export individual visualization components."""
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        scatter = ax1.scatter(self.history_A, self.history_anti_A, 
                             c=self.history_paradox_scores, cmap='RdYlBu_r',
                             s=30, alpha=0.7)
        ax1.set_title(f'Phase Space: {self.system_name}', fontsize=14)
        ax1.set_xlabel('A Value')
        ax1.set_ylabel('¬A Value')
        ax1.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax1, label='Paradox Score')
        plt.tight_layout()
        plt.savefig(f"{base_filename}_phase_space.png", dpi=120, bbox_inches='tight')
        plt.close(fig1)
        
        fig2, (ax2a, ax2b) = plt.subplots(2, 1, figsize=(12, 8))
        
        ax2a.plot(self.history_A, 'b-', label='A', alpha=0.8)
        ax2a.plot(self.history_anti_A, 'r--', label='¬A', alpha=0.8)
        ax2a.set_title('System State Evolution', fontsize=12)
        ax2a.set_xlabel('Step')
        ax2a.set_ylabel('Value')
        ax2a.legend()
        ax2a.grid(True, alpha=0.3)
        
        ax2b.plot(self.history_XEPTQLRI, 'green', label='XEPTQLRI', alpha=0.8)
        ax2b.plot(self.history_paradox_scores, 'purple', label='Paradox Score', alpha=0.8)
        ax2b.set_title('Risk and Paradox Indicators', fontsize=12)
        ax2b.set_xlabel('Step')
        ax2b.set_ylabel('Score')
        ax2b.legend()
        ax2b.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{base_filename}_timeseries.png", dpi=120, bbox_inches='tight')
        plt.close(fig2)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        stage_counts = [np.sum(np.array(self.history_stages) == i) for i in range(10)]
        colors = ['#2E8B57', '#FFD700', '#FF8C00', '#DC143C', '#8A2BE2', 
                 '#000000', '#FF00FF', '#00FFFF', '#FF1493', '#9400D3']
        bars = ax3.bar(range(10), stage_counts, color=colors, alpha=0.8)
        ax3.set_title('Dialectical Stage Distribution', fontsize=14)
        ax3.set_xlabel('Stage')
        ax3.set_ylabel('Count')
        ax3.set_xticks(range(10))
        ax3.set_xticklabels([f'τ{i}' for i in range(10)], rotation=45)
        
        for bar, count in zip(bars, stage_counts):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f"{base_filename}_stages.png", dpi=120, bbox_inches='tight')
        plt.close(fig3)
    
    # ============================================================================
    # UTILITY FUNCTIONS
    # ============================================================================
    
    def get_system_summary(self):
        """Get a quick summary of the system state."""
        if not self.history_XEPTQLRI:
            return "System not yet simulated"
        
        report = self.enhanced_analysis_report()
        
        summary = (
            f"System: {self.system_name}\n"
            f"ID: {self.system_id}\n"
            f"Steps: {len(self.history_A)}\n"
            f"Current Stage: {report['current_state']['stage']}\n"
            f"True State: {report['true_system_state']}\n"
            f"Max XEPTQLRI: {report['metrics']['max_XEPTQLRI']:.3f}\n"
            f"Paradox Events: {report['paradox_analysis']['total_paradox_events']}\n"
            f"Risk Events: {len(self.risk_events)}\n"
            f"Deception Index: {report['metrics']['stability_deception']:.3f}"
        )
        
        return summary
    
    def reset_system(self):
        """Reset the system to initial state."""
        self.history_A = []
        self.history_anti_A = []
        self.history_tension = []
        self.history_XEPTQLRI = []
        self.history_true_XEPTQLRI = []
        self.history_stages = []
        self.history_true_stages = []
        self.history_paradox_scores = []
        self.risk_events = []
        self.paradox_events = []
        self.phase_history = []
        
        print(f"✅ System {self.system_name} reset to initial state")


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demonstrate_paradox_detection():
    """
    Demonstrate the enhanced paradox detection capabilities.
    """
    print("\n" + "="*80)
    print("DEMONSTRATION: PARADOX DETECTION IN XENOPOULOS SYSTEMS")
    print("="*80)
    
    systems = {
        'apparently_stable': XenopoulosGeneticHistoricalSystem(
            initial_state_A=0.2,
            historical_horizon=150,
            aufhebung_threshold=0.9,
            volatility_factor=0.01,
            system_name="Apparently Stable System",
            seed=42
        ),
        
        'paradoxical_transcendence': XenopoulosGeneticHistoricalSystem(
            initial_state_A=0.7,
            historical_horizon=200,
            aufhebung_threshold=0.65,
            volatility_factor=0.05,
            system_name="Paradoxical Transcendence System",
            seed=123
        ),
        
        'false_stability': XenopoulosGeneticHistoricalSystem(
            initial_state_A=0.85,
            historical_horizon=180,
            aufhebung_threshold=0.8,
            volatility_factor=0.02,
            system_name="False Stability System",
            seed=456
        ),
        
        'dynamic_chaos': XenopoulosGeneticHistoricalSystem(
            initial_state_A=0.5,
            historical_horizon=250,
            aufhebung_threshold=0.7,
            volatility_factor=0.1,
            system_name="Dynamic Chaos System",
            seed=789
        )
    }
    
    results = {}
    
    for name, system in systems.items():
        print(f"\n🔍 ANALYZING: {system.system_name}")
        print(f"   ID: {system.system_id}")
        
        system.simulate_enhanced_historical_process()
        report = system.enhanced_analysis_report()
        
        results[name] = {
            'system': system,
            'report': report,
            'true_state': report['true_system_state']
        }
        
        print(f"   📊 True System State: {report['true_system_state']}")
        print(f"   ⚠️  Risk Events: {len(system.risk_events)}")
        print(f"   🔮 Paradox Events: {len(system.paradox_events)}")
        print(f"   🎭 Final Stage: {system.stages[system.history_stages[-1]]}")
        print(f"   📈 Max XEPTQLRI: {report['metrics']['max_XEPTQLRI']:.3f}")
        print(f"   🧠 Mean Paradox Score: {report['metrics']['mean_paradox_score']:.3f}")
    
    return results


def quick_analysis(initial_A=0.5, horizon=200, threshold=0.7, 
                  volatility=0.03, name="Quick Analysis", seed=None):
    """
    Quick analysis function for immediate use.
    """
    print(f"\n⚡ QUICK ANALYSIS: {name}")
    print("-"*50)
    
    system = XenopoulosGeneticHistoricalSystem(
        initial_state_A=initial_A,
        historical_horizon=horizon,
        aufhebung_threshold=threshold,
        volatility_factor=volatility,
        system_name=name,
        seed=seed
    )
    
    system.simulate_enhanced_historical_process()
    report = system.enhanced_analysis_report()
    
    print(f"\n📋 QUICK RESULTS:")
    print(f"   True System State: {report['true_system_state']}")
    print(f"   Max XEPTQLRI: {report['metrics']['max_XEPTQLRI']:.3f}")
    print(f"   Mean Paradox Score: {report['metrics']['mean_paradox_score']:.3f}")
    print(f"   Stability Deception: {report['metrics']['stability_deception']:.3f}")
    print(f"   Risk Events: {len(system.risk_events)}")
    print(f"   Paradox Events: {len(system.paradox_events)}")
    print(f"   Current Stage: {report['current_state']['stage']}")
    
    print(f"\n💡 KEY RECOMMENDATIONS:")
    for i, rec in enumerate(report['recommendations'][:3], 1):
        print(f"   {i}. {rec}")
    
    return system, report


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Main execution with interactive options.
    """
    
    print("\n" + "="*80)
    print("ENHANCED XENOPOULOS SYSTEM v2.0 - MAIN MENU")
    print("="*80)
    print("\n⚠️  FEATURING PARADOX DETECTION & TRUE STABILITY ANALYSIS")
    
    print("\nSelect an option:")
    print("1. Run Paradox Detection Demonstration")
    print("2. Quick Analysis")
    print("3. Create Custom System")
    print("4. Exit")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print("\n🚀 LAUNCHING PARADOX DETECTION DEMONSTRATION...")
            results = demonstrate_paradox_detection()
            
        elif choice == "2":
            print("\n⚡ QUICK ANALYSIS SETUP")
            print("-"*40)
            
            initial_A = float(input("Initial state A (0-1): ") or "0.5")
            horizon = int(input("Simulation horizon: ") or "200")
            threshold = float(input("Aufhebung threshold (0.5-0.95): ") or "0.7")
            volatility = float(input("Volatility factor (0.01-0.2): ") or "0.03")
            name = input("System name: ") or "Quick Analysis System"
            seed = input("Random seed (optional): ") or None
            seed = int(seed) if seed and seed.isdigit() else None
            
            system, report = quick_analysis(initial_A, horizon, threshold, volatility, name, seed)
            
            export_choice = input("\nExport comprehensive analysis? (y/n): ").lower().strip()
            if export_choice == 'y':
                system.export_comprehensive_analysis()
                print("✅ Analysis exported!")
            
        elif choice == "3":
            print("\n🔧 CREATE CUSTOM SYSTEM")
            print("-"*40)
            
            initial_A = float(input("Initial state A (0-1): ") or "0.5")
            horizon = int(input("Simulation horizon: ") or "200")
            threshold = float(input("Aufhebung threshold (0.5-0.95): ") or "0.7")
            volatility = float(input("Volatility factor (0.01-0.2): ") or "0.03")
            name = input("System name: ") or "Custom System"
            seed = input("Random seed (optional): ") or None
            seed = int(seed) if seed and seed.isdigit() else None
            
            system = XenopoulosGeneticHistoricalSystem(
                initial_state_A=initial_A,
                historical_horizon=horizon,
                aufhebung_threshold=threshold,
                volatility_factor=volatility,
                system_name=name,
                seed=seed
            )
            
            print(f"\n🔍 ANALYZING CUSTOM SYSTEM: {name}")
            system.simulate_enhanced_historical_process()
            
            fig = system.create_paradox_detection_dashboard()
            plt.show()
            
            report = system.enhanced_analysis_report()
            print(f"\n📊 CUSTOM SYSTEM REPORT:")
            print(f"   True System State: {report['true_system_state']}")
            print(f"   Max XEPTQLRI: {report['metrics']['max_XEPTQLRI']:.3f}")
            print(f"   Paradox Events: {report['paradox_analysis']['total_paradox_events']}")
            print(f"   Stability Deception: {report['metrics']['stability_deception']:.3f}")
            
            export_choice = input("\nExport comprehensive analysis? (y/n): ").lower().strip()
            if export_choice == 'y':
                system.export_comprehensive_analysis()
                print("✅ Custom analysis exported!")
            
        elif choice == "4":
            print("Exiting Enhanced Xenopoulos System v2.0...")
            
        else:
            print("❌ Invalid choice. Please enter 1-4.")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Program interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()

    print("\n" + "="*80)
    print("ENHANCED XENOPOULOS SYSTEM v2.0 - ANALYSIS COMPLETE")
    print("="*80)
    print("⚠️  Remember: Stability may be an illusion!")
    print("🔍 Always check for: Paradoxical Transcendence, False Stability, Simultaneous Extremity")

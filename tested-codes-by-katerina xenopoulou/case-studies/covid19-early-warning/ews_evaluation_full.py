

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xenopoulos COVID-19 Early Warning System (EWS) Evaluation
Author: Katerina Xenopoulou
ORCID: https://orcid.org/0009-0004-9057-7432
Repository: https://github.com/kxenopoulou/xenopoulos_dialectical-paradoxes-XEPTQLRI
License: CC BY-NC 4.0

This script performs quantitative evaluation of the τ-system's early warning capability.
It detects outbreak events, calculates lead time, signal stability, crisis depth,
and produces a normalized EWS Score (0-1).

Usage:
    python ews_evaluation_full.py \
        --cases covid19_greece_raw.csv \
        --stages xenopoulos_covid19_results.csv \
        --output ews_results.json \
        --language el

Dependencies: pandas, numpy, matplotlib, seaborn, scipy, json
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import find_peaks
import json
import argparse
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')



# ============================================================================
# CONFIGURATION
# ============================================================================

class EWSConfig:
    """Configuration parameters for EWS evaluation."""
    
    # Outbreak detection thresholds
    CASES_THRESHOLD = 1000  # 7-day smoothed cases
    INCREASE_THRESHOLD = 2.0  # 200% increase
    INCREASE_WINDOW = 7  # days
    
    # EWS scoring weights
    LEAD_TIME_WEIGHT = 0.5
    STABILITY_WEIGHT = 0.3
    DEPTH_WEIGHT = 0.2
    
    # Lead time normalization (30 days = perfect score)
    LEAD_TIME_NORMALIZATION = 30
    
    # Visualization
    FIGSIZE = (14, 8)
    COLOR_PALETTE = {
        'τ₄': '#FFA07A',  # Light Salmon - System Saturation
        'τ₃': '#FF6347',  # Tomato - Meaning Incompatibility  
        'τ₂': '#DC143C',  # Crimson - Anomaly Repetition
        'τ₈': '#9370DB',  # Medium Purple - Permanent Dialectics
        'τ₅': '#98FB98',  # Pale Green - Qualitative Leap
        'τ₀': '#D3D3D3',  # Light Gray - Coherence
        'default': '#87CEEB'  # Sky Blue
    }


# ============================================================================
# CORE EWS EVALUATION ENGINE
# ============================================================================

class XenopoulosEWSEvaluator:
    """
    Quantitative evaluation of Xenopoulos τ-system as Early Warning System.
    
    This class implements the methodology described in:
    "A Dialectical Early Warning System for Pandemic Phase Transitions" (2026)
    """
    
    def __init__(self, cases_file, stages_file, language='en'):
        """
        Initialize evaluator with COVID-19 and τ-stage data.
        
        Args:
            cases_file: Path to covid19_greece_raw.csv
            stages_file: Path to xenopoulos_covid19_results.csv
            language: 'en' or 'el' for output labels
        """
        self.language = language
        self.labels = self._get_labels(language)
        
        # Load and validate data
        self.df_cases = self._load_cases(cases_file)
        self.df_stages = self._load_stages(stages_file)
        self.df = self._merge_datasets()
        
        # Detect outbreak events and warnings
        self.outbreaks = self._detect_outbreak_events()
        self.warnings = self._detect_τ_warnings()
        self.results = self._evaluate_all_waves()
        
    def _get_labels(self, language):
        """Return localized labels for plots and reports."""
        if language == 'el':
            return {
                'title_lead': 'Χρόνος Προειδοποίησης ανά Κύμα',
                'title_ews': 'Δείκτης Έγκαιρης Προειδοποίησης (ΣΕΠ)',
                'x_wave': 'Κύμα',
                'y_lead': 'Ημέρες Πριν την Έξαρση',
                'y_ews': 'Δείκτης ΣΕΠ (0-1)',
                'lead_time': 'Χρόνος Προειδοποίησης',
                'stage': 'Στάδιο',
                'ews_score': 'Δείκτης ΣΕΠ',
                'outbreak': 'Έναρξη Έξαρσης',
                'warning': 'Πρώτη Προειδοποίηση τ',
                'table_caption': 'Ποσοτική Αξιολόγηση ΣΕΠ ανά Πανδημικό Κύμα'
            }
        else:
            return {
                'title_lead': 'Early Warning Lead Time by Wave',
                'title_ews': 'Early Warning Score (EWS)',
                'x_wave': 'Wave',
                'y_lead': 'Days Before Outbreak',
                'y_ews': 'EWS Score (0-1)',
                'lead_time': 'Lead Time',
                'stage': 'Stage',
                'ews_score': 'EWS Score',
                'outbreak': 'Outbreak Start',
                'warning': 'First τ Warning',
                'table_caption': 'Quantitative EWS Evaluation per Pandemic Wave'
            }
    
    def _load_cases(self, filepath):
        """Load and preprocess COVID-19 case data."""
        df = pd.read_csv(filepath, parse_dates=['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        # Ensure we have smoothed cases
        if 'new_cases_smoothed' not in df.columns:
            df['new_cases_smoothed'] = df['new_cases'].rolling(7, center=True).mean()
        
        # Forward fill any missing values
        df['new_cases_smoothed'] = df['new_cases_smoothed'].fillna(method='bfill').fillna(method='ffill')
        
        return df
    
    def _load_stages(self, filepath):
        """Load and preprocess τ-stage data."""
        df = pd.read_csv(filepath, parse_dates=['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        # Map stage names for consistency
        stage_mapping = {
            'τ₀: Coherence': 'τ₀',
            'τ₁: First Anomaly': 'τ₁',
            'τ₂: Anomaly Repetition': 'τ₂',
            'τ₃: Meaning Incompatibility': 'τ₃',
            'τ₄: System Saturation': 'τ₄',
            'τ₅: Qualitative Leap': 'τ₅',
            'τ₆: Paradoxical Transcendence': 'τ₆',
            'τ₇: False Stability': 'τ₇',
            'τ₈: Permanent Dialectics': 'τ₈',
            'τ₉: Meta-Transcendence': 'τ₉'
        }
        
        if 'stage' in df.columns:
            df['stage_short'] = df['stage'].map(stage_mapping).fillna(df['stage'])
        else:
            df['stage_short'] = df['stage']
            
        return df
    
    def _merge_datasets(self):
        """Merge cases and stages on date."""
        df = pd.merge(self.df_cases, self.df_stages, on='date', how='inner')
        return df
    
    def _detect_outbreak_events(self):
        """
        Automatically detect major outbreak events.
        
        An outbreak is defined as:
        1. First day smoothed cases > CASES_THRESHOLD, OR
        2. > INCREASE_THRESHOLD (200%) increase within INCREASE_WINDOW days
        """
        df = self.df.copy()
        events = []
        
        # Calculate rolling increases
        df['pct_change_7d'] = df['new_cases_smoothed'].pct_change(periods=7)
        
        # Find threshold exceedances
        threshold_events = df[df['new_cases_smoothed'] > EWSConfig.CASES_THRESHOLD].copy()
        
        # Find rapid increase events
        rapid_events = df[df['pct_change_7d'] > (EWSConfig.INCREASE_THRESHOLD - 1)].copy()
        
        # Combine and deduplicate
        if not threshold_events.empty:
            first_threshold = threshold_events.iloc[0]
            events.append({
                'wave_id': 1,
                'date': first_threshold['date'],
                'cases': first_threshold['new_cases_smoothed'],
                'type': 'threshold',
                'description': f'First >{EWSConfig.CASES_THRESHOLD} cases'
            })
            
        if not rapid_events.empty:
            for _, row in rapid_events.iterrows():
                # Avoid duplicates near threshold events
                if not any(abs((row['date'] - e['date']).days) < 15 for e in events):
                    events.append({
                        'wave_id': len(events) + 1,
                        'date': row['date'],
                        'cases': row['new_cases_smoothed'],
                        'type': 'rapid_increase',
                        'description': f'{row["pct_change_7d"]*100:.0f}% increase in 7 days'
                    })
        
        # Manual overrides for known major waves (ensures completeness)
        known_waves = [
            ('2020-03-05', 'First wave'),
            ('2020-08-04', 'Summer wave'),
            ('2020-11-04', 'Autumn wave'),
            ('2021-03-09', 'Third wave'),
            ('2021-11-09', 'Delta wave')
        ]
        
        for i, (date, desc) in enumerate(known_waves):
            date = pd.to_datetime(date)
            # Check if already detected
            if not any(e['date'] == date for e in events):
                row = df[df['date'] == date].iloc[0]
                events.append({
                    'wave_id': len(events) + 1,
                    'date': date,
                    'cases': row['new_cases_smoothed'],
                    'type': 'manual',
                    'description': desc
                })
        
        # Sort by date and reassign wave IDs
        events = sorted(events, key=lambda x: x['date'])
        for i, event in enumerate(events):
            event['wave_id'] = i + 1
            
        return events
    
    def _detect_τ_warnings(self):
        """
        Detect first τ₄ or higher warning for each outbreak.
        Also identifies τ₃, τ₂, τ₈ as deep crisis signals.
        """
        warnings = []
        
        for outbreak in self.outbreaks:
            outbreak_date = outbreak['date']
            wave_id = outbreak['wave_id']
            
            # Look for warnings before outbreak (up to 2 years prior)
            prior_df = self.df[self.df['date'] < outbreak_date].copy()
            prior_df = prior_df[prior_df['date'] > (outbreak_date - pd.Timedelta(days=730))]
            
            if prior_df.empty:
                continue
                
            # Find first τ₄ or higher
            τ_mask = prior_df['stage_idx'] >= 4
            τ_warnings = prior_df[τ_mask]
            
            if not τ_warnings.empty:
                first_warning = τ_warnings.iloc[0]
                
                # Calculate lead time
                lead_days = (outbreak_date - first_warning['date']).days
                
                # Check stability: stage stable in last 7 days before outbreak?
                pre_outbreak = self.df[
                    (self.df['date'] >= outbreak_date - pd.Timedelta(days=7)) &
                    (self.df['date'] < outbreak_date)
                ]
                
                if not pre_outbreak.empty:
                    unique_stages = pre_outbreak['stage_idx'].nunique()
                    stability = 1 if unique_stages <= 2 else 0
                else:
                    stability = 0
                
                # Get stage at outbreak
                outbreak_row = self.df[self.df['date'] == outbreak_date]
                if not outbreak_row.empty:
                    stage_at_outbreak = outbreak_row.iloc[0]['stage_idx']
                    stage_name = outbreak_row.iloc[0].get('stage_short', f'τ{stage_at_outbreak}')
                else:
                    stage_at_outbreak = 0
                    stage_name = 'unknown'
                
                warnings.append({
                    'wave_id': wave_id,
                    'outbreak_date': outbreak_date,
                    'warning_date': first_warning['date'],
                    'lead_days': lead_days,
                    'stage_idx': first_warning['stage_idx'],
                    'stage_name': first_warning.get('stage_short', f"τ{first_warning['stage_idx']}"),
                    'tension': first_warning['tension'],
                    'stability': stability,
                    'stage_at_outbreak': stage_at_outbreak,
                    'stage_at_outbreak_name': stage_name
                })
            else:
                # No warning found
                warnings.append({
                    'wave_id': wave_id,
                    'outbreak_date': outbreak_date,
                    'warning_date': None,
                    'lead_days': None,
                    'stage_idx': None,
                    'stage_name': 'No warning',
                    'tension': None,
                    'stability': 0,
                    'stage_at_outbreak': None,
                    'stage_at_outbreak_name': None
                })
                
        return warnings
    
    def _calculate_ews_score(self, lead_days, stability, stage_idx):
        """
        Calculate normalized Early Warning Score (0-1).
        
        EWS = min( (L/30)*0.5 + S*0.3 + (D/8)*0.2, 1.0 )
        """
        if lead_days is None or pd.isna(lead_days):
            return 0.0
            
        # Normalize lead time (cap at 30 days for max score)
        lead_norm = min(lead_days / EWSConfig.LEAD_TIME_NORMALIZATION, 1.0)
        
        # Normalize depth
        depth_norm = stage_idx / 8.0 if stage_idx is not None else 0
        
        # Calculate weighted score
        score = (lead_norm * EWSConfig.LEAD_TIME_WEIGHT +
                stability * EWSConfig.STABILITY_WEIGHT +
                depth_norm * EWSConfig.DEPTH_WEIGHT)
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def _evaluate_all_waves(self):
        """Generate complete evaluation results for all waves."""
        results = []
        
        for warning in self.warnings:
            wave_id = warning['wave_id']
            
            # Find matching outbreak
            outbreak = next((o for o in self.outbreaks if o['wave_id'] == wave_id), None)
            
            if outbreak is None:
                continue
                
            # Calculate EWS score
            ews_score = self._calculate_ews_score(
                warning['lead_days'],
                warning['stability'],
                warning['stage_idx']
            )
            
            results.append({
                'wave_id': wave_id,
                'outbreak_date': outbreak['date'].strftime('%Y-%m-%d'),
                'outbreak_description': outbreak['description'],
                'outbreak_cases': round(outbreak['cases'], 1),
                'warning_date': warning['warning_date'].strftime('%Y-%m-%d') if warning['warning_date'] else None,
                'lead_days': warning['lead_days'],
                'stage': warning['stage_name'],
                'stage_idx': warning['stage_idx'],
                'tension': round(warning['tension'], 3) if warning['tension'] else None,
                'stability': warning['stability'],
                'stage_at_outbreak': warning['stage_at_outbreak_name'],
                'ews_score': round(ews_score, 3),
                'success': ews_score >= 0.7
            })
            
        return results
    
    def summary_table(self):
        """Generate pandas DataFrame of results."""
        return pd.DataFrame(self.results)
    
    def plot_lead_time(self, save_path=None):
        """Plot lead time bar chart."""
        df = self.summary_table()
        df = df[df['lead_days'].notna()].copy()
        
        fig, ax = plt.subplots(figsize=EWSConfig.FIGSIZE)
        
        # Color by stage
        colors = []
        for stage in df['stage']:
            base_stage = stage.split(':')[0].strip() if ':' in stage else stage
            colors.append(EWSConfig.COLOR_PALETTE.get(base_stage, EWSConfig.COLOR_PALETTE['default']))
        
        bars = ax.bar(df['wave_id'].astype(str), df['lead_days'], color=colors)
        
        # Add value labels on bars
        for bar, lead, stage in zip(bars, df['lead_days'], df['stage']):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                   f'{int(lead)}d\n{stage}', ha='center', va='bottom', fontsize=10)
        
        ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Optimal (30 days)')
        ax.set_xlabel(self.labels['x_wave'])
        ax.set_ylabel(self.labels['y_lead'])
        ax.set_title(self.labels['title_lead'], fontsize=14, fontweight='bold')
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
            
        return fig
    
    def plot_ews_scores(self, save_path=None):
        """Plot EWS Score bar chart."""
        df = self.summary_table()
        
        fig, ax = plt.subplots(figsize=EWSConfig.FIGSIZE)
        
        # Color by success
        colors = ['#28a745' if s else '#dc3545' for s in df['success']]
        
        bars = ax.bar(df['wave_id'].astype(str), df['ews_score'], color=colors)
        
        # Add value labels on bars
        for bar, score, stage in zip(bars, df['ews_score'], df['stage']):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                   f'{score:.2f}\n{stage}', ha='center', va='bottom', fontsize=10)
        
        ax.axhline(y=0.7, color='orange', linestyle='--', alpha=0.7, label='Success threshold (0.7)')
        ax.set_ylim(0, 1.1)
        ax.set_xlabel(self.labels['x_wave'])
        ax.set_ylabel(self.labels['y_ews'])
        ax.set_title(self.labels['title_ews'], fontsize=14, fontweight='bold')
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
            
        return fig
    
    def plot_timeline(self, save_path=None):
        """Plot complete timeline with cases, stages, and warnings."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)
        
        # Plot 1: Cases
        ax1.plot(self.df['date'], self.df['new_cases_smoothed'], 
                color='black', linewidth=1, alpha=0.7, label='7-day avg cases')
        ax1.set_ylabel('New Cases (smoothed)')
        ax1.set_title('COVID-19 Greece: Cases and τ-Stage Warnings', fontweight='bold')
        ax1.legend(loc='upper left')
        ax1.grid(alpha=0.3)
        
        # Mark outbreaks
        for outbreak in self.outbreaks:
            ax1.axvline(x=outbreak['date'], color='red', linestyle='--', alpha=0.5, linewidth=1)
            ax1.text(outbreak['date'], ax1.get_ylim()[1]*0.9, 
                    f'  W{outbreak["wave_id"]}', rotation=90, va='top', fontsize=9)
        
        # Plot 2: τ-stages
        stage_map = {f'τ{i}': i for i in range(10)}
        self.df['stage_numeric'] = self.df['stage_short'].map(stage_map).fillna(self.df['stage_idx'])
        
        ax2.scatter(self.df['date'], self.df['stage_numeric'], 
                   c=self.df['tension'], cmap='viridis', s=15, alpha=0.6, 
                   label='τ-stage (color = tension)')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('τ-Stage')
        ax2.set_yticks(range(10))
        ax2.set_yticklabels([f'τ{i}' for i in range(10)])
        ax2.legend(loc='upper left')
        ax2.grid(alpha=0.3)
        
        # Mark warnings
        for warning in self.warnings:
            if warning['warning_date']:
                ax2.axvline(x=warning['warning_date'], color='blue', linestyle=':', alpha=0.7, linewidth=1)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
            
        return fig
    
    def generate_latex_table(self):
        """Generate LaTeX table for publication."""
        df = self.summary_table()
        
        if self.language == 'el':
            latex = r"""
\begin{table}[ht]
\centering
\caption{Ποσοτική Αξιολόγηση Συστήματος Έγκαιρης Προειδοποίησης (ΣΕΠ) ανά Πανδημικό Κύμα}
\label{tab:ews_evaluation_el}
\begin{tabular}{ccccccc}
\hline
\hline
Κύμα & Ημ/νία Έξαρσης & Πρώτη Προειδοποίηση & Στάδιο & Χρόνος Προειδ. & Δείκτης ΣΕΠ & Επιτυχία \\
 & & & & (ημέρες) & (0-1) & \\
\hline
"""
        else:
            latex = r"""
\begin{table}[ht]
\centering
\caption{Quantitative Early Warning System (EWS) Evaluation per Pandemic Wave}
\label{tab:ews_evaluation}
\begin{tabular}{ccccccc}
\hline
\hline
Wave & Outbreak Date & First Warning & Stage & Lead Time & EWS Score & Success \\
 & & & & (days) & (0-1) & \\
\hline
"""
        
        for _, row in df.iterrows():
            success_symbol = '✓' if row['success'] else '✗'
            lead_str = f"{int(row['lead_days'])}" if not pd.isna(row['lead_days']) else '—'
            warning_str = row['warning_date'] if row['warning_date'] else '—'
            
            latex += f"{int(row['wave_id'])} & {row['outbreak_date']} & {warning_str} & {row['stage']} & {lead_str} & {row['ews_score']:.2f} & {success_symbol} \\\\\n"
        
        latex += r"""\hline
\hline
\end{tabular}
\end{table}
"""
        return latex
    
    def generate_markdown_table(self):
        """Generate Markdown table for README."""
        df = self.summary_table()
        
        if self.language == 'el':
            header = "| Κύμα | Ημ/νία Έξαρσης | Πρώτη Προειδοποίηση | Στάδιο | Χρόνος Προειδ. (ημέρες) | Δείκτης ΣΕΠ | Επιτυχία |\n"
            header += "|------|-----------------|---------------------|--------|-------------------------|-------------|----------|\n"
        else:
            header = "| Wave | Outbreak Date | First Warning | Stage | Lead Time (days) | EWS Score | Success |\n"
            header += "|------|---------------|---------------|-------|------------------|-----------|---------|\n"
        
        rows = ""
        for _, row in df.iterrows():
            success_symbol = '✅' if row['success'] else '❌'
            lead_str = f"{int(row['lead_days'])}" if not pd.isna(row['lead_days']) else '—'
            warning_str = row['warning_date'] if row['warning_date'] else '—'
            
            rows += f"| {int(row['wave_id'])} | {row['outbreak_date']} | {warning_str} | {row['stage']} | {lead_str} | {row['ews_score']:.2f} | {success_symbol} |\n"
        
        return header + rows
    
    def export_results(self, json_path):
        """Export complete results to JSON."""
        output = {
            'metadata': {
                'evaluation_date': datetime.now().strftime('%Y-%m-%d'),
                'language': self.language,
                'config': {
                    'cases_threshold': EWSConfig.CASES_THRESHOLD,
                    'increase_threshold': f"{EWSConfig.INCREASE_THRESHOLD*100}%",
                    'lead_time_weight': EWSConfig.LEAD_TIME_WEIGHT,
                    'stability_weight': EWSConfig.STABILITY_WEIGHT,
                    'depth_weight': EWSConfig.DEPTH_WEIGHT,
                    'lead_time_normalization': EWSConfig.LEAD_TIME_NORMALIZATION
                }
            },
            'outbreaks': self.outbreaks,
            'warnings': self.warnings,
            'evaluation': self.results,
            'summary': {
                'total_waves': len(self.results),
                'successful_warnings': sum(1 for r in self.results if r['success']),
                'failed_warnings': sum(1 for r in self.results if not r['success']),
                'avg_lead_time': np.mean([r['lead_days'] for r in self.results if r['lead_days']]),
                'avg_ews_score': np.mean([r['ews_score'] for r in self.results])
            }
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        return output


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Xenopoulos COVID-19 Early Warning System Evaluation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ews_evaluation_full.py --cases covid19_greece_raw.csv --stages xenopoulos_covid19_results.csv --output ews_results.json
  python ews_evaluation_full.py --cases data/cases.csv --stages data/stages.csv --language el --output reports/ews_el.json
        """
    )
    
    parser.add_argument('--cases', required=True, help='Path to covid19_greece_raw.csv')
    parser.add_argument('--stages', required=True, help='Path to xenopoulos_covid19_results.csv')
    parser.add_argument('--output', default='ews_results.json', help='Output JSON path')
    parser.add_argument('--language', choices=['en', 'el'], default='en', help='Report language')
    parser.add_argument('--figures', action='store_true', help='Generate figures')
    parser.add_argument('--figures_dir', default='figures', help='Directory to save figures')
    parser.add_argument('--table_format', choices=['markdown', 'latex', 'both'], default='both', 
                       help='Table output format')
    
    args = parser.parse_args()
    
    print(f"\n🚀 Xenopoulos COVID-19 Early Warning System Evaluation")
    print(f"   Language: {args.language}")
    print(f"   Cases: {args.cases}")
    print(f"   Stages: {args.stages}")
    print(f"   Output: {args.output}\n")
    
    # Initialize evaluator
    evaluator = XenopoulosEWSEvaluator(
        cases_file=args.cases,
        stages_file=args.stages,
        language=args.language
    )
    
    # Print summary
    df = evaluator.summary_table()
    print("\n📊 Evaluation Results:")
    print(df.to_string(index=False))
    
    # Export JSON
    evaluator.export_results(args.output)
    print(f"\n💾 Results saved to: {args.output}")
    
    # Generate tables
    if args.table_format in ['markdown', 'both']:
        md_table = evaluator.generate_markdown_table()
        md_path = args.output.replace('.json', '_table.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_table)
        print(f"📄 Markdown table saved to: {md_path}")
    
    if args.table_format in ['latex', 'both']:
        latex_table = evaluator.generate_latex_table()
        latex_path = args.output.replace('.json', '_table.tex')
        with open(latex_path, 'w', encoding='utf-8') as f:
            f.write(latex_table)
        print(f"📄 LaTeX table saved to: {latex_path}")
    
    # Generate figures
    if args.figures:
        os.makedirs(args.figures_dir, exist_ok=True)
        
        lead_path = os.path.join(args.figures_dir, f'figure_lead_time_{args.language}.png')
        evaluator.plot_lead_time(save_path=lead_path)
        print(f"📊 Lead time figure saved to: {lead_path}")
        
        ews_path = os.path.join(args.figures_dir, f'figure_ews_scores_{args.language}.png')
        evaluator.plot_ews_scores(save_path=ews_path)
        print(f"📊 EWS scores figure saved to: {ews_path}")
        
        timeline_path = os.path.join(args.figures_dir, f'figure_timeline_{args.language}.png')
        evaluator.plot_timeline(save_path=timeline_path)
        print(f"📊 Timeline figure saved to: {timeline_path}")
    
    # Print summary statistics
    summary = {
        'total_waves': len(df),
        'successful': df['success'].sum(),
        'failed': len(df) - df['success'].sum(),
        'avg_lead': df['lead_days'].mean(),
        'max_lead': df['lead_days'].max(),
        'min_lead': df['lead_days'].min(),
        'avg_ews': df['ews_score'].mean()
    }
    
    print("\n" + "="*60)
    print("🎯 EARLY WARNING SYSTEM PERFORMANCE SUMMARY")
    print("="*60)
    print(f"   Total waves analyzed:      {summary['total_waves']}")
    print(f"   Successful warnings:       {summary['successful']} ({summary['successful']/summary['total_waves']*100:.1f}%)")
    print(f"   Failed warnings:           {summary['failed']} ({summary['failed']/summary['total_waves']*100:.1f}%)")
    print(f"   Average lead time:         {summary['avg_lead']:.1f} days")
    print(f"   Maximum lead time:         {summary['max_lead']:.0f} days")
    print(f"   Average EWS Score:         {summary['avg_ews']:.3f}")
    print("="*60)
    
    print("\n✅ Evaluation complete.")
    
    return evaluator


if __name__ == '__main__':
    evaluator = main()

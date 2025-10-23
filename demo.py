#!/usr/bin/env python3
"""
Demo script for the recommendation system.

This script demonstrates the recommendation system with various test scenarios
and shows logging and traceability features.
"""

import json
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from src.recommendation_system import RecommendationEngine
from src.recommendation_system.test_scenarios import get_test_scenarios, print_scenario


def print_recommendations(recommendations, verbose=False):
    """Pretty-print recommendations"""
    if not recommendations:
        print("\n  ✓ No recommendations - setup looks optimal!")
        return
    
    print(f"\n  Generated {len(recommendations)} recommendations:\n")
    
    for i, rec in enumerate(recommendations, 1):
        priority_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
        }
        emoji = priority_emoji.get(rec.priority.value, "⚪")
        
        print(f"  {emoji} {i}. [{rec.priority.value.upper()}] {rec.title}")
        print(f"      {rec.description}")
        
        if rec.estimated_monthly_benefit:
            print(f"      💰 Estimated monthly benefit: €{rec.estimated_monthly_benefit:.2f}")
        
        if verbose:
            print(f"      📊 Confidence: {rec.confidence_score:.0%}")
            print(f"      📝 Rationale: {rec.rationale}")
            print(f"      🔖 Rule IDs: {', '.join(rec.rule_ids)}")
        
        print()


def run_demo(scenario_name=None, verbose=False):
    """Run the demo for specific or all scenarios"""
    print("="*70)
    print("  Sabsteck API - Recommendation System Demo")
    print("="*70)
    
    # Initialize the recommendation engine
    print("\n📦 Initializing Recommendation Engine...")
    engine = RecommendationEngine(enable_ml=True)
    
    # Get system info
    system_info = engine.get_system_info()
    print(f"  ✓ Rule Engine: {len(system_info['rule_engine']['rules'])} rules loaded")
    print(f"  ✓ ML Engine: {'Enabled' if system_info['ml_engine']['enabled'] else 'Disabled'}")
    
    # Get test scenarios
    scenarios = get_test_scenarios()
    
    # Filter to specific scenario if requested
    if scenario_name:
        if scenario_name not in scenarios:
            print(f"\n❌ Error: Scenario '{scenario_name}' not found")
            print(f"\nAvailable scenarios: {', '.join(scenarios.keys())}")
            return
        scenarios = {scenario_name: scenarios[scenario_name]}
    
    # Process each scenario
    for name, setup in scenarios.items():
        print_scenario(name, setup)
        
        # Get recommendations
        print("\n🔍 Analyzing income setup...")
        recommendations = engine.get_recommendations(setup)
        print_recommendations(recommendations, verbose=verbose)
        
        # Get summary
        if verbose:
            print("📊 Summary Statistics:")
            summary = engine.get_recommendations_summary(setup)
            print(f"  • Total recommendations: {summary['total_recommendations']}")
            print(f"  • Total estimated benefit: €{summary['total_estimated_monthly_benefit']:.2f}")
            print(f"  • By priority: {summary['recommendations_by_priority']}")
            print()
        
        print("-" * 70)


def run_interactive():
    """Run interactive mode for custom income setups"""
    from src.recommendation_system.models import (
        IncomeSetup,
        IncomeSource,
        IncomeType,
        TaxClass,
    )
    
    print("="*70)
    print("  Interactive Mode - Create Custom Income Setup")
    print("="*70)
    
    try:
        # Basic info
        person_id = input("\nPerson ID: ").strip() or "custom_001"
        tax_class = input("Tax Class (1-6): ").strip() or "1"
        monthly_expenses = float(input("Monthly Expenses (EUR): ").strip() or "2000")
        
        # Income sources
        income_sources = []
        print("\nAdd income sources (press Enter when done):")
        
        while True:
            print("\nIncome Types: salary, freelance, investment, rental, business, passive")
            income_type = input("  Income Type: ").strip().lower()
            if not income_type:
                break
            
            try:
                amount = float(input("  Monthly Amount (EUR): ").strip())
                description = input("  Description (optional): ").strip()
                
                income_sources.append(
                    IncomeSource(
                        income_type=IncomeType(income_type),
                        monthly_amount=amount,
                        description=description or None,
                    )
                )
                print(f"  ✓ Added {income_type}: €{amount}")
            except (ValueError, KeyError) as e:
                print(f"  ❌ Invalid input: {e}")
        
        if not income_sources:
            print("\n❌ No income sources added. Exiting.")
            return
        
        # Create setup
        setup = IncomeSetup(
            person_id=person_id,
            income_sources=income_sources,
            tax_class=TaxClass(tax_class),
            monthly_expenses=monthly_expenses,
        )
        
        # Get recommendations
        print("\n" + "="*70)
        print("  Analyzing Your Income Setup")
        print("="*70)
        
        print_scenario("custom", setup)
        
        print("\n🔍 Generating recommendations...")
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(setup)
        print_recommendations(recommendations, verbose=True)
        
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Recommendation System Demo")
    parser.add_argument(
        "--scenario",
        "-s",
        help="Run specific scenario",
        choices=[
            "single_salary",
            "high_earner_no_diversification",
            "diversified_good_savings",
            "freelancer_concentrated",
            "low_savings_critical",
            "negative_disposable",
            "high_concentration",
            "optimal_setup",
        ],
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed information",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode",
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive()
    else:
        run_demo(scenario_name=args.scenario, verbose=args.verbose)


if __name__ == "__main__":
    main()

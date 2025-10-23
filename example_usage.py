#!/usr/bin/env python3
"""
Simple example showing how to use the Recommendation System.
"""

from src.recommendation_system import (
    RecommendationEngine,
    IncomeSetup,
    IncomeSource,
    IncomeType,
    TaxClass,
)


def main():
    print("=" * 60)
    print("Recommendation System - Simple Example")
    print("=" * 60)
    
    # Example 1: Single salary earner
    print("\n📋 Example 1: Single Salary Earner")
    print("-" * 60)
    
    setup1 = IncomeSetup(
        person_id="example_001",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=3500.0,
                is_primary=True,
                description="Software Developer"
            )
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=2800.0,
    )
    
    print(f"Monthly Income: €{setup1.total_monthly_income:.2f}")
    print(f"Monthly Expenses: €{setup1.monthly_expenses:.2f}")
    print(f"Disposable Income: €{setup1.disposable_income:.2f}")
    
    engine = RecommendationEngine()
    recommendations = engine.get_recommendations(setup1)
    
    print(f"\n💡 Recommendations: {len(recommendations)}")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. [{rec.priority.value.upper()}] {rec.title}")
        print(f"   {rec.description}")
        if rec.estimated_monthly_benefit:
            print(f"   Potential benefit: €{rec.estimated_monthly_benefit:.2f}/month")
    
    # Example 2: Diversified income with good savings
    print("\n\n📋 Example 2: Diversified Income")
    print("-" * 60)
    
    setup2 = IncomeSetup(
        person_id="example_002",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=4000.0,
                is_primary=True,
            ),
            IncomeSource(
                income_type=IncomeType.INVESTMENT,
                monthly_amount=800.0,
                description="ETF Portfolio"
            ),
            IncomeSource(
                income_type=IncomeType.RENTAL,
                monthly_amount=600.0,
                description="Rental Property"
            ),
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=3200.0,
        savings_goal=1500.0,
    )
    
    print(f"Monthly Income: €{setup2.total_monthly_income:.2f}")
    print(f"  - Salary: €4000.00")
    print(f"  - Investment: €800.00")
    print(f"  - Rental: €600.00")
    print(f"Monthly Expenses: €{setup2.monthly_expenses:.2f}")
    print(f"Disposable Income: €{setup2.disposable_income:.2f}")
    print(f"Savings Rate: {(setup2.disposable_income / setup2.total_monthly_income * 100):.1f}%")
    
    recommendations2 = engine.get_recommendations(setup2)
    
    if recommendations2:
        print(f"\n💡 Recommendations: {len(recommendations2)}")
        for i, rec in enumerate(recommendations2, 1):
            print(f"\n{i}. [{rec.priority.value.upper()}] {rec.title}")
            print(f"   {rec.description}")
    else:
        print("\n✅ No recommendations - Your income setup looks well-optimized!")
    
    # Example 3: Using the summary feature
    print("\n\n📋 Example 3: Recommendations Summary")
    print("-" * 60)
    
    summary = engine.get_recommendations_summary(setup1)
    
    print(f"Person ID: {summary['person_id']}")
    print(f"Total Recommendations: {summary['total_recommendations']}")
    print(f"Total Estimated Benefit: €{summary['total_estimated_monthly_benefit']:.2f}/month")
    print(f"By Priority: {summary['recommendations_by_priority']}")
    
    print("\n" + "=" * 60)
    print("Done! Check DOCUMENTATION.md for more details.")
    print("=" * 60)


if __name__ == "__main__":
    main()

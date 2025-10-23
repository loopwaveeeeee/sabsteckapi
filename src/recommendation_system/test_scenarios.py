"""Test scenarios for the recommendation system"""

from .models import (
    IncomeSetup,
    IncomeSource,
    IncomeType,
    TaxClass,
)


def get_test_scenarios():
    """
    Get predefined test scenarios for the recommendation system.
    
    Returns:
        Dictionary of test scenario names to IncomeSetup objects
    """
    scenarios = {}
    
    # Scenario 1: Single income source (salary only)
    scenarios["single_salary"] = IncomeSetup(
        person_id="person_001",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=3500.0,
                is_primary=True,
                description="Full-time software developer",
            )
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=2800.0,
        savings_goal=500.0,
        metadata={"scenario": "single_salary", "description": "Single income, moderate expenses"},
    )
    
    # Scenario 2: High earner with no diversification
    scenarios["high_earner_no_diversification"] = IncomeSetup(
        person_id="person_002",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=7500.0,
                is_primary=True,
                description="Senior manager position",
            )
        ],
        tax_class=TaxClass.CLASS_3,
        monthly_expenses=4500.0,
        savings_goal=2000.0,
        metadata={"scenario": "high_earner", "description": "High income, potential for optimization"},
    )
    
    # Scenario 3: Diversified income with good savings
    scenarios["diversified_good_savings"] = IncomeSetup(
        person_id="person_003",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=4000.0,
                is_primary=True,
                description="Primary employment",
            ),
            IncomeSource(
                income_type=IncomeType.INVESTMENT,
                monthly_amount=800.0,
                description="ETF dividends and interest",
            ),
            IncomeSource(
                income_type=IncomeType.RENTAL,
                monthly_amount=600.0,
                description="Rental property income",
            ),
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=3200.0,
        savings_goal=1500.0,
        metadata={"scenario": "diversified", "description": "Well-diversified, good savings rate"},
    )
    
    # Scenario 4: Freelancer with high income concentration
    scenarios["freelancer_concentrated"] = IncomeSetup(
        person_id="person_004",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.FREELANCE,
                monthly_amount=5000.0,
                is_primary=True,
                description="Freelance consulting",
            ),
            IncomeSource(
                income_type=IncomeType.FREELANCE,
                monthly_amount=1000.0,
                description="Side projects",
            ),
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=3500.0,
        savings_goal=1000.0,
        metadata={"scenario": "freelancer", "description": "Freelance income, potential for business structure"},
    )
    
    # Scenario 5: Low savings rate (critical)
    scenarios["low_savings_critical"] = IncomeSetup(
        person_id="person_005",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=2500.0,
                is_primary=True,
                description="Entry-level position",
            )
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=2300.0,
        metadata={"scenario": "low_savings", "description": "Very low savings rate, needs optimization"},
    )
    
    # Scenario 6: Negative disposable income (critical)
    scenarios["negative_disposable"] = IncomeSetup(
        person_id="person_006",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=2000.0,
                is_primary=True,
                description="Part-time work",
            ),
            IncomeSource(
                income_type=IncomeType.FREELANCE,
                monthly_amount=500.0,
                description="Occasional freelance work",
            ),
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=2800.0,
        metadata={"scenario": "negative", "description": "Expenses exceed income - critical situation"},
    )
    
    # Scenario 7: High income concentration with multiple sources
    scenarios["high_concentration"] = IncomeSetup(
        person_id="person_007",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=6000.0,
                is_primary=True,
                description="Primary job",
            ),
            IncomeSource(
                income_type=IncomeType.FREELANCE,
                monthly_amount=500.0,
                description="Side work",
            ),
            IncomeSource(
                income_type=IncomeType.PASSIVE,
                monthly_amount=300.0,
                description="Small passive income",
            ),
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=4000.0,
        savings_goal=1500.0,
        metadata={"scenario": "concentrated", "description": "Multiple sources but highly concentrated"},
    )
    
    # Scenario 8: Optimal setup (minimal recommendations expected)
    scenarios["optimal_setup"] = IncomeSetup(
        person_id="person_008",
        income_sources=[
            IncomeSource(
                income_type=IncomeType.SALARY,
                monthly_amount=4500.0,
                is_primary=True,
                description="Stable employment",
            ),
            IncomeSource(
                income_type=IncomeType.INVESTMENT,
                monthly_amount=1200.0,
                description="Diversified investment portfolio",
            ),
            IncomeSource(
                income_type=IncomeType.BUSINESS,
                monthly_amount=800.0,
                description="Small business income",
            ),
            IncomeSource(
                income_type=IncomeType.PASSIVE,
                monthly_amount=500.0,
                description="Passive income streams",
            ),
        ],
        tax_class=TaxClass.CLASS_1,
        monthly_expenses=4000.0,
        savings_goal=2000.0,
        metadata={"scenario": "optimal", "description": "Well-optimized setup"},
    )
    
    return scenarios


def print_scenario(scenario_name: str, setup: IncomeSetup):
    """Pretty-print a test scenario"""
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario_name}")
    print(f"{'='*60}")
    print(f"Person ID: {setup.person_id}")
    print(f"Tax Class: {setup.tax_class.value}")
    print(f"\nIncome Sources ({len(setup.income_sources)}):")
    for i, source in enumerate(setup.income_sources, 1):
        print(f"  {i}. {source.income_type.value}: €{source.monthly_amount:.2f}")
        if source.description:
            print(f"     ({source.description})")
    print(f"\nTotal Monthly Income: €{setup.total_monthly_income:.2f}")
    print(f"Monthly Expenses: €{setup.monthly_expenses:.2f}")
    print(f"Disposable Income: €{setup.disposable_income:.2f}")
    if setup.savings_goal:
        print(f"Savings Goal: €{setup.savings_goal:.2f}")
    print(f"\nMetadata: {setup.metadata}")


if __name__ == "__main__":
    # Print all scenarios when run directly
    scenarios = get_test_scenarios()
    for name, setup in scenarios.items():
        print_scenario(name, setup)

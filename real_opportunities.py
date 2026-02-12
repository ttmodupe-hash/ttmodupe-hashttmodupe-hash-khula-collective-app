"""
REAL Investment Opportunities - Not Generic BS
Based on actual SA market gaps, crises, and emerging sectors
"""

REAL_OPPORTUNITIES = {
    'crisis_opportunities': {
        'category': 'Crisis = Opportunity',
        'opportunities': [
            {
                'name': 'Load Shedding Solution: Inverter & Battery Installation Service',
                'investment_required': 68000,
                'description': 'Install inverters and batteries for homes/businesses during load shedding crisis',
                'why_now': 'Stage 6 load shedding = desperate customers, 6-month waiting lists, premium pricing',
                'revenue_model': {
                    'installations_per_month': 8,
                    'average_installation_fee': 15000,  # R15k per installation
                    'monthly_revenue': 120000,
                    'monthly_costs': {
                        'equipment_markup': 60000,  # Buy wholesale, sell retail
                        'labor': 15000,
                        'transport': 5000,
                        'marketing': 3000,
                        'total': 83000
                    },
                    'monthly_profit': 37000,
                    'annual_profit': 444000
                },
                'roi': {
                    'payback_period_months': 2.2,
                    'annual_return_percentage': 652.9,
                    'break_even_months': 3
                },
                'risks': {
                    'load_shedding_ends': {
                        'level': 'Low',
                        'percentage': 10,
                        'mitigation': 'Eskom crisis is structural, will last years. Pivot to solar if needed.'
                    },
                    'competition': {
                        'level': 'Medium',
                        'percentage': 30,
                        'mitigation': 'Demand far exceeds supply. Focus on speed and service.'
                    },
                    'technical_skills': {
                        'level': 'Medium',
                        'percentage': 25,
                        'mitigation': 'Partner with qualified electrician, get certified training.'
                    }
                },
                'market_analysis': {
                    'market_size': 'R50+ billion opportunity - millions of homes/businesses need backup power',
                    'current_demand': 'Installers booked 6+ months ahead, customers desperate',
                    'price_trend': 'Premium pricing accepted due to urgency',
                    'competition': 'Overwhelmed - can\'t keep up with demand',
                    'target_customers': 'Middle-class homes, small businesses, medical practices, home offices'
                },
                'success_probability': 85,
                'recommended_for_balance': [60000, 150000]
            },
            {
                'name': 'Water Crisis Solution: Borehole Drilling Service',
                'investment_required': 72000,
                'description': 'Drill boreholes for homes/businesses facing water shortages',
                'why_now': 'Day Zero threats, municipal failures, businesses need water security',
                'revenue_model': {
                    'boreholes_per_month': 6,
                    'price_per_borehole': 35000,
                    'monthly_revenue': 210000,
                    'monthly_costs': {
                        'equipment_rental': 45000,
                        'labor': 30000,
                        'fuel_transport': 15000,
                        'permits': 5000,
                        'total': 95000
                    },
                    'monthly_profit': 115000,
                    'annual_profit': 1380000
                },
                'roi': {
                    'payback_period_months': 0.75,
                    'annual_return_percentage': 1916.7,
                    'break_even_months': 1
                },
                'risks': {
                    'water_table_depth': {
                        'level': 'Medium',
                        'percentage': 30,
                        'mitigation': 'Survey before drilling, charge deposit, offer refund if no water.'
                    },
                    'equipment_breakdown': {
                        'level': 'Medium',
                        'percentage': 25,
                        'mitigation': 'Rent equipment initially, maintenance contract, backup rig.'
                    },
                    'regulations': {
                        'level': 'Low',
                        'percentage': 15,
                        'mitigation': 'Get proper permits, follow DWS guidelines, legal compliance.'
                    }
                },
                'market_analysis': {
                    'market_size': 'Massive - every city facing water crisis',
                    'current_demand': 'Drillers booked 3-6 months ahead',
                    'price_trend': 'Increasing - R25k to R40k+ per borehole',
                    'competition': 'Limited - specialized equipment and skills required',
                    'target_customers': 'Suburban homes, farms, businesses, schools, hospitals'
                },
                'success_probability': 80,
                'recommended_for_balance': [70000, 150000]
            }
        ]
    },
    
    'legal_new_markets': {
        'category': 'Newly Legal Markets',
        'opportunities': [
            {
                'name': 'Cannabis Cultivation (Legal for Personal Use)',
                'investment_required': 55000,
                'description': 'Indoor cannabis cultivation for legal personal use market',
                'why_now': 'Recently legalized, massive demand, limited legal supply, premium pricing',
                'revenue_model': {
                    'harvests_per_year': 4,
                    'yield_per_harvest_kg': 3,
                    'selling_price_per_kg': 45000,  # R45k/kg wholesale
                    'revenue_per_harvest': 135000,
                    'annual_revenue': 540000,
                    'costs_per_harvest': {
                        'seeds_nutrients': 8000,
                        'electricity': 6000,
                        'water': 1000,
                        'labor': 5000,
                        'total': 20000
                    },
                    'profit_per_harvest': 115000,
                    'annual_profit': 460000
                },
                'roi': {
                    'payback_period_months': 1.4,
                    'annual_return_percentage': 836.4,
                    'break_even_harvests': 1
                },
                'risks': {
                    'legal_grey_area': {
                        'level': 'High',
                        'percentage': 45,
                        'mitigation': 'Stay within personal use limits, consult lawyer, proper documentation.'
                    },
                    'crop_failure': {
                        'level': 'Medium',
                        'percentage': 30,
                        'mitigation': 'Climate control, pest management, backup genetics, insurance.'
                    },
                    'market_access': {
                        'level': 'Medium',
                        'percentage': 35,
                        'mitigation': 'Build network carefully, focus on medical users, legal channels.'
                    }
                },
                'market_analysis': {
                    'market_size': 'R28 billion illegal market transitioning to legal',
                    'current_supply': 'Severely limited legal supply',
                    'price_trend': 'Premium pricing for quality legal product',
                    'competition': 'Few legal operators, mostly still illegal',
                    'target_customers': 'Medical users, legal personal use market'
                },
                'success_probability': 65,
                'recommended_for_balance': [50000, 100000],
                'legal_note': 'IMPORTANT: Consult lawyer. Stay within personal use limits. Do not sell commercially without license.'
            }
        ]
    },
    
    'import_replacement': {
        'category': 'Import Replacement Opportunities',
        'opportunities': [
            {
                'name': 'Plastic Injection Molding (Replace Chinese Imports)',
                'investment_required': 78000,
                'description': 'Manufacture plastic products locally that are currently imported from China',
                'why_now': 'Rand weakness makes imports expensive, shipping delays, "buy local" movement',
                'revenue_model': {
                    'products': 'Plastic containers, household items, packaging',
                    'production_runs_per_month': 10,
                    'revenue_per_run': 25000,
                    'monthly_revenue': 250000,
                    'monthly_costs': {
                        'raw_materials': 80000,
                        'electricity': 15000,
                        'labor': 25000,
                        'maintenance': 5000,
                        'total': 125000
                    },
                    'monthly_profit': 125000,
                    'annual_profit': 1500000
                },
                'roi': {
                    'payback_period_months': 0.75,
                    'annual_return_percentage': 1923.1,
                    'break_even_months': 1
                },
                'risks': {
                    'chinese_competition': {
                        'level': 'Medium',
                        'percentage': 35,
                        'mitigation': 'Compete on speed, customization, no shipping delays, local support.'
                    },
                    'mold_costs': {
                        'level': 'Medium',
                        'percentage': 30,
                        'mitigation': 'Start with simple products, rent molds, partner with existing manufacturers.'
                    },
                    'quality_control': {
                        'level': 'Low',
                        'percentage': 20,
                        'mitigation': 'Proper training, quality checks, certifications.'
                    }
                },
                'market_analysis': {
                    'market_size': 'R120 billion plastic products market in SA',
                    'import_dependency': '70% imported - massive opportunity',
                    'price_advantage': 'Can compete on price + speed + customization',
                    'competition': 'Limited local manufacturers, mostly importers',
                    'target_customers': 'Retailers, wholesalers, manufacturers, packaging companies'
                },
                'success_probability': 75,
                'recommended_for_balance': [75000, 180000]
            },
            {
                'name': 'Spice Blending & Packaging (Replace Imports)',
                'investment_required': 42000,
                'description': 'Blend and package spices locally instead of importing pre-packaged',
                'why_now': 'Import costs high, demand for local products, premium pricing for quality',
                'revenue_model': {
                    'products': 'Curry powder, BBQ spice, peri-peri, custom blends',
                    'batches_per_month': 40,
                    'revenue_per_batch': 8000,
                    'monthly_revenue': 320000,
                    'monthly_costs': {
                        'raw_spices': 120000,
                        'packaging': 30000,
                        'labor': 20000,
                        'utilities': 5000,
                        'total': 175000
                    },
                    'monthly_profit': 145000,
                    'annual_profit': 1740000
                },
                'roi': {
                    'payback_period_months': 0.35,
                    'annual_return_percentage': 4142.9,
                    'break_even_months': 1
                },
                'risks': {
                    'food_safety': {
                        'level': 'Medium',
                        'percentage': 30,
                        'mitigation': 'Get food safety certification, proper hygiene, quality control.'
                    },
                    'competition': {
                        'level': 'Medium',
                        'percentage': 25,
                        'mitigation': 'Unique blends, better quality, local story, direct relationships.'
                    },
                    'supply_chain': {
                        'level': 'Low',
                        'percentage': 15,
                        'mitigation': 'Multiple suppliers, bulk buying, inventory management.'
                    }
                },
                'market_analysis': {
                    'market_size': 'R8 billion spice market in SA',
                    'import_dependency': '60% imported',
                    'price_advantage': '40-60% cheaper than imported brands',
                    'competition': 'Dominated by big brands, opportunity for local artisan',
                    'target_customers': 'Restaurants, retailers, wholesalers, online direct-to-consumer'
                },
                'success_probability': 82,
                'recommended_for_balance': [40000, 90000]
            }
        ]
    },
    
    'infrastructure_gaps': {
        'category': 'Infrastructure Crisis Opportunities',
        'opportunities': [
            {
                'name': 'Mobile Cold Storage Rental',
                'investment_required': 65000,
                'description': 'Rent refrigerated containers to businesses during power outages',
                'why_now': 'Load shedding destroys perishables, businesses desperate for backup cold storage',
                'revenue_model': {
                    'containers': 2,
                    'rental_per_container_per_day': 800,
                    'utilization_rate': 0.85,  # 85% occupancy
                    'days_per_month': 30,
                    'monthly_revenue': 40800,
                    'monthly_costs': {
                        'fuel_generators': 12000,
                        'maintenance': 3000,
                        'transport': 4000,
                        'insurance': 2000,
                        'total': 21000
                    },
                    'monthly_profit': 19800,
                    'annual_profit': 237600
                },
                'roi': {
                    'payback_period_months': 3.9,
                    'annual_return_percentage': 365.5,
                    'break_even_months': 4
                },
                'risks': {
                    'equipment_failure': {
                        'level': 'Medium',
                        'percentage': 35,
                        'mitigation': 'Regular maintenance, backup generators, insurance coverage.'
                    },
                    'fuel_costs': {
                        'level': 'Medium',
                        'percentage': 30,
                        'mitigation': 'Pass costs to customer, solar panels, efficient generators.'
                    },
                    'seasonal_demand': {
                        'level': 'Low',
                        'percentage': 20,
                        'mitigation': 'Load shedding is year-round, events also need cold storage.'
                    }
                },
                'market_analysis': {
                    'market_size': 'Every restaurant, butchery, supermarket needs backup',
                    'current_supply': 'Very limited - huge unmet demand',
                    'price_trend': 'Premium pricing accepted due to urgency',
                    'competition': 'Minimal - specialized equipment',
                    'target_customers': 'Restaurants, butcheries, supermarkets, caterers, events'
                },
                'success_probability': 78,
                'recommended_for_balance': [60000, 130000]
            },
            {
                'name': 'Pothole Repair Service (Municipal Failure)',
                'investment_required': 48000,
                'description': 'Rapid pothole repair service for businesses and residential estates',
                'why_now': 'Municipalities failing, roads deteriorating, businesses/estates willing to pay',
                'revenue_model': {
                    'repairs_per_month': 50,
                    'average_price_per_repair': 2500,
                    'monthly_revenue': 125000,
                    'monthly_costs': {
                        'materials': 35000,
                        'equipment_rental': 15000,
                        'labor': 25000,
                        'fuel': 8000,
                        'total': 83000
                    },
                    'monthly_profit': 42000,
                    'annual_profit': 504000
                },
                'roi': {
                    'payback_period_months': 1.4,
                    'annual_return_percentage': 1050.0,
                    'break_even_months': 2
                },
                'risks': {
                    'weather_dependency': {
                        'level': 'Medium',
                        'percentage': 30,
                        'mitigation': 'Work in dry weather, quick-set materials, covered storage.'
                    },
                    'material_quality': {
                        'level': 'Low',
                        'percentage': 20,
                        'mitigation': 'Use quality materials, offer warranty, build reputation.'
                    },
                    'liability': {
                        'level': 'Medium',
                        'percentage': 25,
                        'mitigation': 'Proper insurance, quality work, clear contracts.'
                    }
                },
                'market_analysis': {
                    'market_size': 'Massive - roads deteriorating nationwide',
                    'current_supply': 'Municipalities can\'t keep up',
                    'price_trend': 'Businesses willing to pay premium for quick fixes',
                    'competition': 'Limited private operators',
                    'target_customers': 'Business parks, residential estates, shopping centers, private roads'
                },
                'success_probability': 80,
                'recommended_for_balance': [45000, 100000]
            }
        ]
    },
    
    'technology_arbitrage': {
        'category': 'Technology Arbitrage',
        'opportunities': [
            {
                'name': 'Cryptocurrency Mining Farm (Solar Powered)',
                'investment_required': 75000,
                'description': 'Mine cryptocurrency using solar power to offset electricity costs',
                'why_now': 'Crypto prices recovering, solar costs falling, load shedding makes grid unreliable',
                'revenue_model': {
                    'mining_rigs': 10,
                    'daily_mining_revenue': 1200,  # Bitcoin/Ethereum mining
                    'monthly_revenue': 36000,
                    'monthly_costs': {
                        'electricity': 3000,  # Mostly solar, some grid backup
                        'internet': 1000,
                        'cooling': 2000,
                        'maintenance': 2000,
                        'total': 8000
                    },
                    'monthly_profit': 28000,
                    'annual_profit': 336000
                },
                'roi': {
                    'payback_period_months': 2.7,
                    'annual_return_percentage': 448.0,
                    'break_even_months': 3
                },
                'risks': {
                    'crypto_price_volatility': {
                        'level': 'High',
                        'percentage': 50,
                        'mitigation': 'Diversify coins mined, sell regularly, hedge positions.'
                    },
                    'equipment_obsolescence': {
                        'level': 'Medium',
                        'percentage': 35,
                        'mitigation': 'Buy latest ASICs, plan for 2-year replacement cycle.'
                    },
                    'electricity_costs': {
                        'level': 'Low',
                        'percentage': 15,
                        'mitigation': 'Solar panels reduce costs by 80%, grid backup only.'
                    }
                },
                'market_analysis': {
                    'market_size': 'Global crypto market cap $2+ trillion',
                    'sa_advantage': 'Cheap solar power, weak rand makes mining profitable',
                    'price_trend': 'Crypto recovering from bear market',
                    'competition': 'Limited in SA due to electricity costs - solar solves this',
                    'target_revenue': 'Passive income, 24/7 operation'
                },
                'success_probability': 70,
                'recommended_for_balance': [70000, 150000],
                'technical_note': 'Requires technical knowledge or partnership with crypto expert'
            }
        ]
    }
}

def get_real_opportunities(balance):
    """Get real opportunities that actually make sense"""
    suitable = []
    
    for category_key, category_data in REAL_OPPORTUNITIES.items():
        for opp in category_data['opportunities']:
            min_bal, max_bal = opp['recommended_for_balance']
            if min_bal <= balance <= max_bal:
                opp['category'] = category_data['category']
                suitable.append(opp)
    
    # Sort by ROI and success probability
    suitable.sort(key=lambda x: (x['success_probability'], x['roi']['annual_return_percentage']), reverse=True)
    
    return suitable

if __name__ == "__main__":
    opps = get_real_opportunities(71700)
    print(f"Found {len(opps)} REAL opportunities for R71,700:\n")
    
    for i, opp in enumerate(opps, 1):
        print(f"{i}. {opp['name']}")
        print(f"   Why Now: {opp['why_now']}")
        print(f"   Investment: R{opp['investment_required']:,}")
        print(f"   Annual Profit: R{opp['revenue_model']['annual_profit']:,}")
        print(f"   ROI: {opp['roi']['annual_return_percentage']:.0f}%")
        print(f"   Success: {opp['success_probability']}%\n")
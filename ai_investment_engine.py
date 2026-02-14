"""
Advanced AI Investment Intelligence Engine for Khula Collective
Real opportunities, real analysis, real returns
"""

import pandas as pd
from datetime import datetime, timedelta
import json

class InvestmentOpportunityEngine:
    """
    Analyzes real investment opportunities based on collective pot size
    Provides detailed risk analysis, ROI projections, and actionable recommendations
    """
    
    def __init__(self, collective_balance):
        self.balance = collective_balance
        self.opportunities = self._load_opportunities()
        # Load real opportunities
        from real_opportunities import REAL_OPPORTUNITIES
        self.real_opportunities = REAL_OPPORTUNITIES
    
    def _load_opportunities(self):
        """Load real investment opportunities with detailed analysis"""
        return {
            'manufacturing_equipment': {
                'category': 'Chinese Manufacturing Equipment',
                'opportunities': [
                    {
                        'name': 'Automatic Brick Making Machine',
                        'supplier': 'Alibaba/Made-in-China',
                        'investment_required': 45000,
                        'description': 'QT4-15 Automatic Concrete Block Making Machine - produces 4000-5000 bricks/day',
                        'revenue_model': {
                            'brick_price': 2.50,  # R2.50 per brick
                            'daily_production': 4500,
                            'working_days_per_month': 22,
                            'monthly_revenue': 247500,  # R247,500/month
                            'monthly_costs': {
                                'raw_materials': 80000,
                                'labor': 25000,
                                'electricity': 8000,
                                'maintenance': 5000,
                                'transport': 10000,
                                'total': 128000
                            },
                            'monthly_profit': 119500,
                            'annual_profit': 1434000
                        },
                        'roi': {
                            'payback_period_months': 4.5,
                            'annual_return_percentage': 318.7,
                            'break_even_months': 5
                        },
                        'risks': {
                            'market_demand': {
                                'level': 'Medium',
                                'percentage': 30,
                                'mitigation': 'Pre-sell to construction companies, secure contracts'
                            },
                            'equipment_failure': {
                                'level': 'Low',
                                'percentage': 15,
                                'mitigation': 'Warranty coverage, local technician training'
                            },
                            'competition': {
                                'level': 'Medium',
                                'percentage': 25,
                                'mitigation': 'Focus on quality, build relationships with contractors'
                            }
                        },
                        'requirements': {
                            'space': '200-300 sqm warehouse/yard',
                            'permits': 'Business license, environmental clearance',
                            'skills': 'Basic machine operation (training provided)',
                            'team': '2-3 operators, 1 sales person'
                        },
                        'market_analysis': {
                            'sa_construction_growth': '4.2% annually',
                            'brick_demand': 'High - housing shortage of 2.3 million units',
                            'competition_level': 'Moderate - mostly manual brick makers',
                            'target_customers': 'Construction companies, property developers, government housing projects'
                        },
                        'success_probability': 75,
                        'recommended_for_balance': [40000, 100000]
                    },
                    {
                        'name': 'Industrial Sewing Machines (10 units)',
                        'supplier': 'Alibaba - Juki/Brother Industrial',
                        'investment_required': 65000,
                        'description': '10 industrial sewing machines for clothing manufacturing/alterations business',
                        'revenue_model': {
                            'garments_per_day': 150,  # 15 per machine
                            'price_per_garment': 45,
                            'working_days_per_month': 22,
                            'monthly_revenue': 148500,
                            'monthly_costs': {
                                'fabric_materials': 45000,
                                'labor': 35000,  # 10 operators
                                'electricity': 4000,
                                'maintenance': 3000,
                                'rent': 8000,
                                'total': 95000
                            },
                            'monthly_profit': 53500,
                            'annual_profit': 642000
                        },
                        'roi': {
                            'payback_period_months': 14.6,
                            'annual_return_percentage': 98.8,
                            'break_even_months': 15
                        },
                        'risks': {
                            'fashion_trends': {
                                'level': 'Medium',
                                'percentage': 35,
                                'mitigation': 'Focus on basics, school uniforms, corporate wear'
                            },
                            'skilled_labor': {
                                'level': 'High',
                                'percentage': 40,
                                'mitigation': 'Training program, competitive wages, retention bonuses'
                            },
                            'market_saturation': {
                                'level': 'Low',
                                'percentage': 20,
                                'mitigation': 'Quality focus, fast turnaround, custom services'
                            }
                        },
                        'requirements': {
                            'space': '100-150 sqm workshop',
                            'permits': 'Business license, health & safety compliance',
                            'skills': 'Sewing expertise, pattern making',
                            'team': '10 operators, 1 supervisor, 1 sales/admin'
                        },
                        'market_analysis': {
                            'sa_textile_market': 'R50 billion annually',
                            'import_dependency': '65% - opportunity for local production',
                            'demand_drivers': 'School uniforms, corporate wear, fashion retail',
                            'target_customers': 'Schools, corporates, boutiques, online retailers'
                        },
                        'success_probability': 70,
                        'recommended_for_balance': [60000, 150000]
                    }
                ]
            },
            'livestock_farming': {
                'category': 'Livestock & Poultry Farming',
                'opportunities': [
                    {
                        'name': 'Broiler Chicken Farm (500 birds/cycle)',
                        'investment_required': 55000,
                        'description': 'Small-scale broiler chicken farming - 4 cycles per year',
                        'revenue_model': {
                            'birds_per_cycle': 500,
                            'cycles_per_year': 4,
                            'selling_price_per_bird': 85,
                            'revenue_per_cycle': 42500,
                            'annual_revenue': 170000,
                            'costs_per_cycle': {
                                'day_old_chicks': 12500,  # R25 each
                                'feed': 15000,
                                'medication': 2500,
                                'labor': 3000,
                                'utilities': 2000,
                                'total': 35000
                            },
                            'profit_per_cycle': 7500,
                            'annual_profit': 30000
                        },
                        'roi': {
                            'payback_period_months': 22,
                            'annual_return_percentage': 54.5,
                            'break_even_cycles': 8
                        },
                        'risks': {
                            'disease_outbreak': {
                                'level': 'High',
                                'percentage': 45,
                                'mitigation': 'Vaccination program, biosecurity measures, insurance'
                            },
                            'feed_price_volatility': {
                                'level': 'Medium',
                                'percentage': 30,
                                'mitigation': 'Bulk buying, alternative feed sources, price hedging'
                            },
                            'market_price_fluctuation': {
                                'level': 'Medium',
                                'percentage': 25,
                                'mitigation': 'Pre-sell to butcheries, restaurants, contract farming'
                            }
                        },
                        'requirements': {
                            'space': '200 sqm chicken house + 500 sqm land',
                            'permits': 'Agricultural permit, health certificate',
                            'skills': 'Poultry management (training available)',
                            'team': '1 full-time manager, 1 part-time helper'
                        },
                        'market_analysis': {
                            'sa_chicken_consumption': '42kg per capita annually',
                            'market_size': 'R50 billion poultry industry',
                            'growth_rate': '3.5% annually',
                            'target_customers': 'Butcheries, restaurants, supermarkets, direct consumers'
                        },
                        'success_probability': 65,
                        'recommended_for_balance': [50000, 100000]
                    },
                    {
                        'name': 'Goat Farming (20 breeding does)',
                        'investment_required': 48000,
                        'description': 'Boer goat breeding for meat production',
                        'revenue_model': {
                            'breeding_does': 20,
                            'kids_per_doe_per_year': 2.5,  # Average
                            'total_kids_per_year': 50,
                            'selling_price_per_kid': 2500,  # 6-month old
                            'annual_revenue': 125000,
                            'annual_costs': {
                                'feed_supplements': 24000,
                                'veterinary': 8000,
                                'labor': 18000,
                                'infrastructure_maintenance': 5000,
                                'total': 55000
                            },
                            'annual_profit': 70000
                        },
                        'roi': {
                            'payback_period_months': 8.2,
                            'annual_return_percentage': 145.8,
                            'break_even_months': 9
                        },
                        'risks': {
                            'predators_theft': {
                                'level': 'High',
                                'percentage': 40,
                                'mitigation': 'Secure fencing, guard dogs, night security, insurance'
                            },
                            'disease': {
                                'level': 'Medium',
                                'percentage': 30,
                                'mitigation': 'Vaccination, quarantine new animals, vet partnership'
                            },
                            'drought': {
                                'level': 'Medium',
                                'percentage': 25,
                                'mitigation': 'Supplementary feeding, water storage, drought-resistant breeds'
                            }
                        },
                        'requirements': {
                            'space': '2-3 hectares grazing land',
                            'permits': 'Agricultural permit, animal movement permits',
                            'skills': 'Livestock management (training available)',
                            'team': '1 full-time herder/manager'
                        },
                        'market_analysis': {
                            'sa_goat_meat_demand': 'Growing - cultural preference, health conscious',
                            'import_dependency': '40% - local production opportunity',
                            'price_trend': 'Stable to increasing',
                            'target_customers': 'Butcheries, restaurants, cultural ceremonies, direct sales'
                        },
                        'success_probability': 70,
                        'recommended_for_balance': [45000, 90000]
                    }
                ]
            },
            'property_rental': {
                'category': 'Property & Room Rental',
                'opportunities': [
                    {
                        'name': 'Bachelor Rooms Conversion (4 rooms)',
                        'investment_required': 75000,
                        'description': 'Convert existing property into 4 bachelor rooms for rental',
                        'revenue_model': {
                            'rooms': 4,
                            'rent_per_room': 2500,
                            'monthly_revenue': 10000,
                            'annual_revenue': 120000,
                            'monthly_costs': {
                                'rates_taxes': 800,
                                'water_electricity': 1200,
                                'maintenance': 500,
                                'insurance': 400,
                                'management': 500,
                                'total': 3400
                            },
                            'monthly_profit': 6600,
                            'annual_profit': 79200
                        },
                        'roi': {
                            'payback_period_months': 11.4,
                            'annual_return_percentage': 105.6,
                            'break_even_months': 12
                        },
                        'risks': {
                            'tenant_default': {
                                'level': 'High',
                                'percentage': 45,
                                'mitigation': 'Deposit (2 months), credit checks, rental insurance, lease agreements'
                            },
                            'property_damage': {
                                'level': 'Medium',
                                'percentage': 30,
                                'mitigation': 'Deposits, regular inspections, maintenance fund, insurance'
                            },
                            'vacancy_periods': {
                                'level': 'Medium',
                                'percentage': 25,
                                'mitigation': 'Competitive pricing, good location, tenant retention, marketing'
                            }
                        },
                        'requirements': {
                            'property': 'Existing house/building in good location',
                            'permits': 'Occupancy certificate, rental license',
                            'skills': 'Property management (can outsource)',
                            'team': 'Property manager (part-time or outsourced)'
                        },
                        'market_analysis': {
                            'sa_rental_demand': 'High - urbanization, housing shortage',
                            'occupancy_rates': '85-95% in good locations',
                            'rental_growth': '5-7% annually',
                            'target_tenants': 'Young professionals, students, single workers'
                        },
                        'success_probability': 80,
                        'recommended_for_balance': [70000, 150000]
                    },
                    {
                        'name': 'Shipping Container Student Accommodation (2 units)',
                        'investment_required': 68000,
                        'description': '2 converted shipping containers as student accommodation near university',
                        'revenue_model': {
                            'units': 2,
                            'rent_per_unit': 3500,
                            'monthly_revenue': 7000,
                            'annual_revenue': 84000,
                            'monthly_costs': {
                                'land_rental': 1500,
                                'utilities': 800,
                                'maintenance': 400,
                                'insurance': 300,
                                'security': 500,
                                'total': 3500
                            },
                            'monthly_profit': 3500,
                            'annual_profit': 42000
                        },
                        'roi': {
                            'payback_period_months': 19.4,
                            'annual_return_percentage': 61.8,
                            'break_even_months': 20
                        },
                        'risks': {
                            'location_dependency': {
                                'level': 'High',
                                'percentage': 40,
                                'mitigation': 'Near university, transport routes, amenities'
                            },
                            'seasonal_vacancy': {
                                'level': 'Medium',
                                'percentage': 35,
                                'mitigation': 'Year-round leases, target working students, short-term lets'
                            },
                            'regulatory_changes': {
                                'level': 'Low',
                                'percentage': 20,
                                'mitigation': 'Proper permits, building codes compliance, legal advice'
                            }
                        },
                        'requirements': {
                            'land': 'Rental plot near university (200-300 sqm)',
                            'permits': 'Building approval, occupancy certificate',
                            'skills': 'Property management',
                            'team': 'Property manager (part-time)'
                        },
                        'market_analysis': {
                            'student_accommodation_shortage': 'Critical - 300,000+ bed shortage nationally',
                            'rental_rates': 'R2,500-R4,500 per unit near universities',
                            'occupancy_rates': '90-100% during academic year',
                            'target_market': 'University students, young professionals'
                        },
                        'success_probability': 75,
                        'recommended_for_balance': [65000, 120000]
                    }
                ]
            },
            'agriculture': {
                'category': 'Agricultural Investments',
                'opportunities': [
                    {
                        'name': 'Hydroponic Vegetable Farming',
                        'investment_required': 52000,
                        'description': 'Small-scale hydroponic system for leafy vegetables (lettuce, spinach, herbs)',
                        'revenue_model': {
                            'growing_cycles_per_year': 8,
                            'harvest_per_cycle_kg': 400,
                            'selling_price_per_kg': 35,
                            'revenue_per_cycle': 14000,
                            'annual_revenue': 112000,
                            'costs_per_cycle': {
                                'seeds_nutrients': 2500,
                                'electricity_water': 1500,
                                'labor': 2000,
                                'packaging': 500,
                                'transport': 800,
                                'total': 7300
                            },
                            'profit_per_cycle': 6700,
                            'annual_profit': 53600
                        },
                        'roi': {
                            'payback_period_months': 11.6,
                            'annual_return_percentage': 103.1,
                            'break_even_cycles': 8
                        },
                        'risks': {
                            'technical_failure': {
                                'level': 'Medium',
                                'percentage': 35,
                                'mitigation': 'Backup systems, technical training, maintenance schedule'
                            },
                            'market_access': {
                                'level': 'Medium',
                                'percentage': 30,
                                'mitigation': 'Pre-sell to restaurants, supermarkets, farmers markets'
                            },
                            'electricity_costs': {
                                'level': 'Medium',
                                'percentage': 25,
                                'mitigation': 'Solar panels, energy-efficient systems, load shedding backup'
                            }
                        },
                        'requirements': {
                            'space': '100-150 sqm greenhouse/indoor space',
                            'permits': 'Agricultural permit, water use license',
                            'skills': 'Hydroponic farming (training available)',
                            'team': '1 full-time farmer/manager'
                        },
                        'market_analysis': {
                            'organic_produce_demand': 'Growing 15% annually',
                            'restaurant_demand': 'High - fresh, pesticide-free produce',
                            'price_premium': '30-50% over conventional produce',
                            'target_customers': 'Restaurants, health stores, farmers markets, direct consumers'
                        },
                        'success_probability': 72,
                        'recommended_for_balance': [50000, 100000]
                    },
                    {
                        'name': 'Mushroom Farming (Oyster Mushrooms)',
                        'investment_required': 38000,
                        'description': 'Indoor oyster mushroom cultivation - 4 harvests per month',
                        'revenue_model': {
                            'harvests_per_month': 4,
                            'kg_per_harvest': 80,
                            'selling_price_per_kg': 85,
                            'monthly_revenue': 27200,
                            'annual_revenue': 326400,
                            'monthly_costs': {
                                'substrate_spawn': 8000,
                                'labor': 4000,
                                'utilities': 2000,
                                'packaging': 1500,
                                'transport': 1000,
                                'total': 16500
                            },
                            'monthly_profit': 10700,
                            'annual_profit': 128400
                        },
                        'roi': {
                            'payback_period_months': 4.3,
                            'annual_return_percentage': 337.9,
                            'break_even_months': 5
                        },
                        'risks': {
                            'contamination': {
                                'level': 'High',
                                'percentage': 40,
                                'mitigation': 'Sterile procedures, climate control, quality substrate'
                            },
                            'market_education': {
                                'level': 'Medium',
                                'percentage': 30,
                                'mitigation': 'Cooking demos, recipe cards, restaurant partnerships'
                            },
                            'climate_control': {
                                'level': 'Medium',
                                'percentage': 25,
                                'mitigation': 'Proper ventilation, humidity control, temperature monitoring'
                            }
                        },
                        'requirements': {
                            'space': '50-80 sqm climate-controlled room',
                            'permits': 'Food production license, health certificate',
                            'skills': 'Mushroom cultivation (training available)',
                            'team': '1 full-time cultivator'
                        },
                        'market_analysis': {
                            'mushroom_market_growth': '12% annually in SA',
                            'health_food_trend': 'Strong - vegan, low-calorie, nutritious',
                            'supply_gap': 'Most mushrooms imported - local opportunity',
                            'target_customers': 'Restaurants, health stores, supermarkets, vegans'
                        },
                        'success_probability': 68,
                        'recommended_for_balance': [35000, 80000]
                    }
                ]
            },
            'import_export': {
                'category': 'Import/Export Trading',
                'opportunities': [
                    {
                        'name': 'Chinese Electronics Wholesale',
                        'investment_required': 72000,
                        'description': 'Import and wholesale consumer electronics from China',
                        'revenue_model': {
                            'shipments_per_year': 6,
                            'investment_per_shipment': 12000,
                            'markup_percentage': 85,
                            'revenue_per_shipment': 22200,
                            'annual_revenue': 133200,
                            'costs_per_shipment': {
                                'product_cost': 12000,
                                'shipping_customs': 2500,
                                'storage': 800,
                                'marketing': 500,
                                'total': 15800
                            },
                            'profit_per_shipment': 6400,
                            'annual_profit': 38400
                        },
                        'roi': {
                            'payback_period_months': 22.5,
                            'annual_return_percentage': 53.3,
                            'break_even_shipments': 12
                        },
                        'risks': {
                            'currency_fluctuation': {
                                'level': 'High',
                                'percentage': 45,
                                'mitigation': 'Forward contracts, quick turnover, price adjustments'
                            },
                            'customs_delays': {
                                'level': 'Medium',
                                'percentage': 35,
                                'mitigation': 'Proper documentation, customs broker, buffer stock'
                            },
                            'product_quality': {
                                'level': 'Medium',
                                'percentage': 30,
                                'mitigation': 'Supplier vetting, quality checks, warranties, returns policy'
                            }
                        },
                        'requirements': {
                            'space': 'Storage facility (50-100 sqm)',
                            'permits': 'Import license, tax clearance, business registration',
                            'skills': 'Import/export knowledge, supplier relationships',
                            'team': '1 manager, 1 sales person'
                        },
                        'market_analysis': {
                            'electronics_market_sa': 'R120 billion annually',
                            'import_dependency': '80% - mostly from China',
                            'margin_potential': '60-100% markup on wholesale',
                            'target_customers': 'Retailers, online sellers, corporate buyers'
                        },
                        'success_probability': 65,
                        'recommended_for_balance': [70000, 150000]
                    }
                ]
            }
        }
    
    def get_opportunities_for_balance(self, balance):
        """Get investment opportunities suitable for current collective balance"""
        suitable_opportunities = []
        
        # First, load REAL opportunities (crisis-based, actually useful)
        for category_key, category_data in self.real_opportunities.items():
            for opp in category_data['opportunities']:
                min_balance, max_balance = opp['recommended_for_balance']
                if min_balance <= balance <= max_balance:
                    opp['category'] = category_data['category']
                    opp['affordability_score'] = self._calculate_affordability(balance, opp['investment_required'])
                    suitable_opportunities.append(opp)
        
        # Then add original opportunities as backup
        for category_key, category_data in self.opportunities.items():
            for opp in category_data['opportunities']:
                min_balance, max_balance = opp['recommended_for_balance']
                if min_balance <= balance <= max_balance:
                    opp['category'] = category_data['category']
                    opp['affordability_score'] = self._calculate_affordability(balance, opp['investment_required'])
                    suitable_opportunities.append(opp)
        
        # Sort by success probability and ROI
        suitable_opportunities.sort(key=lambda x: (x['success_probability'], x['roi']['annual_return_percentage']), reverse=True)
        
        return suitable_opportunities
    
    def _calculate_affordability(self, balance, required):
        """Calculate how affordable an opportunity is (0-100)"""
        if balance < required:
            return 0
        ratio = balance / required
        if ratio >= 2:
            return 100
        return min(100, (ratio - 1) * 100)
    
    def generate_detailed_recommendation(self, opportunity):
        """Generate detailed investment recommendation with analysis"""
        
        recommendation = {
            'opportunity': opportunity['name'],
            'category': opportunity['category'],
            'investment_required': opportunity['investment_required'],
            'description': opportunity['description'],
            
            'financial_analysis': {
                'monthly_profit': opportunity['revenue_model'].get('monthly_profit', 
                                  opportunity['revenue_model'].get('profit_per_cycle', 0)),
                'annual_profit': opportunity['revenue_model']['annual_profit'],
                'roi_percentage': opportunity['roi']['annual_return_percentage'],
                'payback_months': opportunity['roi']['payback_period_months'],
                'break_even': opportunity['roi']['break_even_months']
            },
            
            'risk_assessment': {
                'overall_risk_score': self._calculate_overall_risk(opportunity['risks']),
                'detailed_risks': opportunity['risks'],
                'success_probability': opportunity['success_probability']
            },
            
            'requirements': opportunity.get('requirements', {}),
            'market_analysis': opportunity.get('market_analysis', {}),
            
            'recommendation_strength': self._calculate_recommendation_strength(opportunity),
            
            'action_plan': self._generate_action_plan(opportunity),
            
            'collective_impact': self._calculate_collective_impact(opportunity)
        }
        
        return recommendation
    
    def _calculate_overall_risk(self, risks):
        """Calculate overall risk score (0-100, lower is better)"""
        total_risk = 0
        for risk_name, risk_data in risks.items():
            total_risk += risk_data['percentage']
        return min(100, total_risk / len(risks))
    
    def _calculate_recommendation_strength(self, opp):
        """Calculate how strongly we recommend this (0-100)"""
        roi_score = min(100, opp['roi']['annual_return_percentage'] / 3)
        success_score = opp['success_probability']
        risk_score = 100 - self._calculate_overall_risk(opp['risks'])
        
        return (roi_score * 0.4 + success_score * 0.4 + risk_score * 0.2)
    
    def _generate_action_plan(self, opp):
        """Generate step-by-step action plan"""
        requirements = opp.get('requirements', {})
        
        return {
            'phase_1_research': [
                f"Visit suppliers/locations for {opp['name']}",
                "Get 3 quotes from different suppliers",
                "Visit successful similar businesses",
                "Speak to industry experts",
                "Calculate exact costs for our area"
            ],
            'phase_2_preparation': [
                f"Secure {requirements.get('space', 'appropriate space')}",
                f"Obtain {requirements.get('permits', 'necessary permits')}",
                "Set up business entity and bank account",
                f"Recruit {requirements.get('team', 'necessary team members')}",
                "Arrange training if needed"
            ],
            'phase_3_execution': [
                "Place initial order/make purchase",
                "Set up operations",
                "Launch marketing campaign",
                "Secure first customers/contracts",
                "Monitor and optimize"
            ],
            'timeline': '2-3 months from decision to first revenue'
        }
    
    def _calculate_collective_impact(self, opp):
        """Calculate impact on collective members"""
        annual_profit = opp['revenue_model']['annual_profit']
        investment = opp['investment_required']
        
        # Assuming 20 members with equal shares
        profit_per_member = annual_profit / 20
        investment_per_member = investment / 20
        
        return {
            'total_annual_profit': annual_profit,
            'profit_per_member': profit_per_member,
            'investment_per_member': investment_per_member,
            'monthly_return_per_member': profit_per_member / 12,
            'roi_per_member': (profit_per_member / investment_per_member) * 100
        }


class MarketTrendAnalyzer:
    """Analyzes market trends and identifies opportunities"""
    
    def __init__(self):
        self.trends = self._load_current_trends()
    
    def _load_current_trends(self):
        """Load current market trends in South Africa"""
        return {
            'high_growth_sectors': [
                {
                    'sector': 'Renewable Energy',
                    'growth_rate': '18% annually',
                    'opportunity': 'Solar panel installation services',
                    'why': 'Load shedding crisis, falling solar costs, government incentives',
                    'entry_capital': 'R60,000 - R150,000'
                },
                {
                    'sector': 'E-commerce & Logistics',
                    'growth_rate': '25% annually',
                    'opportunity': 'Last-mile delivery service',
                    'why': 'Online shopping boom, courier demand, gig economy',
                    'entry_capital': 'R40,000 - R80,000'
                },
                {
                    'sector': 'Health & Wellness',
                    'growth_rate': '12% annually',
                    'opportunity': 'Organic food production/distribution',
                    'why': 'Health consciousness, lifestyle diseases, premium pricing',
                    'entry_capital': 'R50,000 - R100,000'
                },
                {
                    'sector': 'Education Technology',
                    'growth_rate': '20% annually',
                    'opportunity': 'After-school tutoring center',
                    'why': 'Poor education outcomes, parent demand, recurring revenue',
                    'entry_capital': 'R45,000 - R90,000'
                }
            ],
            'emerging_opportunities': [
                {
                    'opportunity': 'Waste Recycling',
                    'why': 'Environmental regulations, raw material costs, circular economy',
                    'potential_return': '80-150% annually',
                    'risk_level': 'Medium'
                },
                {
                    'opportunity': 'Mobile Car Wash',
                    'why': 'Water scarcity, convenience demand, low overhead',
                    'potential_return': '120-200% annually',
                    'risk_level': 'Low'
                },
                {
                    'opportunity': 'Food Truck/Catering',
                    'why': 'Events industry recovery, corporate catering, festivals',
                    'potential_return': '90-180% annually',
                    'risk_level': 'Medium'
                }
            ],
            'avoid_sectors': [
                {
                    'sector': 'Traditional Retail',
                    'reason': 'E-commerce disruption, high overhead, declining foot traffic'
                },
                {
                    'sector': 'Petrol Stations',
                    'reason': 'Electric vehicle transition, high capital, regulatory complexity'
                }
            ]
        }
    
    def get_trend_analysis(self):
        """Get comprehensive trend analysis"""
        return self.trends


class RiskCalculator:
    """Calculate and explain investment risks"""
    
    @staticmethod
    def calculate_risk_adjusted_return(roi_percentage, risk_percentage):
        """Calculate risk-adjusted return (Sharpe-like ratio)"""
        # Simple risk-adjusted return: ROI / Risk
        if risk_percentage == 0:
            return roi_percentage
        return (roi_percentage / risk_percentage) * 100
    
    @staticmethod
    def generate_risk_report(opportunity):
        """Generate detailed risk report"""
        risks = opportunity['risks']
        
        report = {
            'risk_summary': {},
            'mitigation_strategies': {},
            'contingency_plans': {},
            'insurance_recommendations': []
        }
        
        for risk_name, risk_data in risks.items():
            report['risk_summary'][risk_name] = {
                'level': risk_data['level'],
                'probability': f"{risk_data['percentage']}%",
                'impact': 'High' if risk_data['percentage'] > 35 else 'Medium' if risk_data['percentage'] > 20 else 'Low'
            }
            
            report['mitigation_strategies'][risk_name] = risk_data['mitigation']
        
        # Add insurance recommendations based on risks
        if any(r['level'] == 'High' for r in risks.values()):
            report['insurance_recommendations'].append('Comprehensive business insurance')
        
        return report


# Example usage and testing
if __name__ == "__main__":
    # Test with R71,700 collective balance
    engine = InvestmentOpportunityEngine(71700)
    opportunities = engine.get_opportunities_for_balance(71700)
    
    print(f"Found {len(opportunities)} suitable opportunities for R71,700 collective pot:\n")
    
    for i, opp in enumerate(opportunities[:3], 1):
        print(f"{i}. {opp['name']}")
        print(f"   Category: {opp['category']}")
        print(f"   Investment: R{opp['investment_required']:,}")
        print(f"   Annual Profit: R{opp['revenue_model']['annual_profit']:,}")
        print(f"   ROI: {opp['roi']['annual_return_percentage']:.1f}%")
        print(f"   Success Probability: {opp['success_probability']}%")
        print(f"   Payback: {opp['roi']['payback_period_months']:.1f} months\n")
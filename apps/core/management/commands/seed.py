import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import transaction
from django.utils.text import slugify

from apps.sectors.models import Sector
from apps.users.models import User, UserProfile, Subscription
from apps.businesses.models import *
from apps.core.models import Source
from apps.core.seed_data.sectors import SECTORS
from apps.core.seed_data.users import USERS, REGULAR_USERS, PROFILES
from apps.core.seed_data.businesses import (
    BUSINESSES, BUSINESS_SCALES, CAPITAL_ITEMS, RISKS,
    FEASIBILITY_FACTORS, FINANCIAL_METRICS
)
from apps.core.seed_data.business_profiles import (
    BUSINESS_PROFILES, BUSINESS_PROFILE_FEATURES, BUSINESS_PROFILE_TESTIMONIALS
)
from apps.core.seed_data.operating_costs import OPERATING_COSTS
from apps.core.seed_data.operations_checklists import OPERATIONS_CHECKLISTS
from apps.core.seed_data.sources import SOURCES
from apps.core.seed_data.intelligence_snapshots import INTELLIGENCE_SNAPSHOTS
from apps.core.seed_data.time_series_metrics import TIME_SERIES_METRICS
from apps.core.seed_data.sector_stats import SECTOR_STATS
from apps.core.seed_data.reports import REPORTS
from apps.core.seed_data.report_bundles import REPORT_BUNDLES
from apps.core.seed_data.countries import COUNTRIES, REGIONS
from apps.content.models import *
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed the database with initial data for GAMBIH'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apps',
            type=str,
            help='Comma-separated list of apps to seed (sectors, users, businesses, profiles, sources, snapshots)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force seeding even if data exists'
        )

    def handle(self, *args, **options):
        apps_to_seed = options.get('apps')
        force = options.get('force', False)
        
        if apps_to_seed:
            apps_list = [app.strip() for app in apps_to_seed.split(',')]
        else:
            apps_list = ['sources', 'countries', 'sectors', 'sector_stats', 'users',
                        'businesses', 'operating_costs', 'checklists', 'profiles',
                        'snapshots', 'time_series', 'content', 'reports', 'report_bundles']
        
        self.stdout.write(self.style.WARNING('Starting database seeding...'))
        
        try:
            with transaction.atomic():
                if 'sources' in apps_list:
                    self.seed_sources(force)

                if 'countries' in apps_list:
                    self.seed_countries(force)

                if 'sectors' in apps_list:
                    self.seed_sectors(force)

                if 'sector_stats' in apps_list:
                    self.seed_sector_stats(force)
                
                if 'users' in apps_list:
                    self.seed_users(force)
                
                if 'businesses' in apps_list:
                    self.seed_businesses(force)
                
                if 'operating_costs' in apps_list:
                    self.seed_operating_costs(force)
                
                if 'checklists' in apps_list:
                    self.seed_operations_checklists(force)
                
                if 'profiles' in apps_list:
                    self.seed_business_profiles(force)
                
                if 'snapshots' in apps_list:
                    self.seed_intelligence_snapshots(force)
                
                if 'time_series' in apps_list:
                    self.seed_time_series_metrics(force)
                
                if 'content' in apps_list:
                    self.seed_content(force)

                if 'reports' in apps_list:
                    self.seed_reports(force)

                if 'report_bundles' in apps_list:
                    self.seed_report_bundles(force)

            self.stdout.write(self.style.SUCCESS('✓ Database seeding completed successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error during seeding: {str(e)}'))
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def seed_sources(self, force=False):
        """Seed sources data"""
        existing_count = Source.objects.count()
        
        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Sources already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            Source.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing sources.'))
        
        sources_created = 0
        for source_data in SOURCES:
            source, created = Source.objects.get_or_create(
                name=source_data['name'],
                year=source_data['year'],
                defaults={
                    'reference': source_data.get('reference', ''),
                    'source_type': source_data['source_type'],
                    'confidence_rating': source_data['confidence_rating'],
                    'is_primary_source': source_data.get('is_primary_source', False),
                    'notes': source_data.get('notes', '')
                }
            )
            if created:
                sources_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {sources_created} sources'))

    def seed_sectors(self, force=False):
        """Seed sectors data"""
        existing_count = Sector.objects.count()
        
        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Sectors already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            Sector.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing sectors.'))
        
        sectors_created = 0
        for sector_data in SECTORS:
            sector, created = Sector.objects.get_or_create(
                name=sector_data['name'],
                defaults={
                    'description': sector_data['description'],
                    'icon': sector_data['icon'],
                    'color': sector_data['color'],
                    'order': sector_data['order'],
                    'status': 'published'
                }
            )
            if created:
                sectors_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {sectors_created} sectors'))

    def seed_users(self, force=False):
        """Seed users data (unchanged - works with existing)"""
        existing_count = User.objects.count()
        
        if existing_count > 1 and not force:
            self.stdout.write(self.style.WARNING(f'  Users already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            User.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing users.'))
        
        users_created = 0
        
        # Create admin and staff users
        for user_data in USERS:
            password = user_data.pop('password', 'Password123')
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    **user_data,
                    'password': make_password(password)
                }
            )
            if created:
                users_created += 1
                UserProfile.objects.get_or_create(user=user)
        
        # Create regular test users
        for user_data in REGULAR_USERS:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True,
                    'tier': 'regular'
                }
            )
            if created:
                user.set_password('Test123456')
                user.save()
                users_created += 1
                UserProfile.objects.get_or_create(user=user)
        
        # Update profiles with additional data
        for profile_data in PROFILES:
            try:
                user = User.objects.get(email=profile_data['user_email'])
                profile, created = UserProfile.objects.get_or_create(user=user)
                for key, value in profile_data.items():
                    if key != 'user_email':
                        setattr(profile, key, value)
                profile.save()
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    User {profile_data["user_email"]} not found'))
        
        # Create subscription for premium user
        try:
            premium_user = User.objects.get(email='premium@e-biz.gm')
            Subscription.objects.get_or_create(
                user=premium_user,
                defaults={
                    'plan_type': 'premium',
                    'amount': 4990,
                    'duration_days': 365,
                    'started_at': timezone.now(),
                    'expires_at': timezone.now() + timedelta(days=365),
                    'is_active': True,
                    'is_paid': True
                }
            )
        except User.DoesNotExist:
            pass
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {users_created} users'))

    def seed_businesses(self, force=False):
        """Seed businesses and related data"""
        existing_count = Business.objects.count()
        
        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Businesses already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            Business.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing businesses.'))
        
        businesses_created = 0
        scales_created = 0
        capital_created = 0
        risks_created = 0
        feasibility_created = 0
        financial_created = 0
        
        # Get default source
        default_source = Source.objects.filter(is_primary_source=True).first()
        
        # Create businesses
        for business_data in BUSINESSES:
            try:
                sector = Sector.objects.get(name=business_data['sector_name'])
                business, created = Business.objects.get_or_create(
                    name=business_data['name'],
                    defaults={
                        'sector': sector,
                        'short_description': business_data['short_description'],
                        'overview': business_data['overview'],
                        'opportunity_thesis': business_data['opportunity_thesis'],
                        'is_featured': business_data.get('is_featured', False),
                        'has_scales': business_data.get('has_scales', True),
                        'status': business_data.get('status', 'published')
                    }
                )
                if created:
                    businesses_created += 1
            except Sector.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Sector {business_data["sector_name"]} not found'))
        
        # Create business scales
        for scale_data in BUSINESS_SCALES:
            try:
                business = Business.objects.get(name=scale_data['business_name'])
                scale, created = BusinessScale.objects.get_or_create(
                    business=business,
                    scale_type=scale_data['scale_type'],
                    year=scale_data['year'],
                    defaults={
                        'capacity_definition': scale_data['capacity_definition'],
                        'target_market': scale_data['target_market'],
                        'location_type': scale_data['location_type'],
                        'labor_needed': scale_data['labor_needed'],
                        'overall_feasibility_score': scale_data.get('overall_feasibility_score'),
                        'primary_source': default_source
                    }
                )
                if created:
                    scales_created += 1
            except Business.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Business {scale_data["business_name"]} not found'))
        
        # Create capital items
        for capital_data in CAPITAL_ITEMS:
            try:
                business = Business.objects.get(name=capital_data['business_name'])
                scale = BusinessScale.objects.get(
                    business=business, 
                    scale_type=capital_data['scale_type'],
                    year=capital_data.get('year', 2024)
                )
                capital, created = CapitalItem.objects.get_or_create(
                    scale=scale,
                    category=capital_data['category'],
                    item_name=capital_data['item_name'],
                    defaults={
                        'quantity': capital_data['quantity'],
                        'unit_cost': capital_data['unit_cost'],
                        'priority': capital_data['priority'],
                        'source': default_source
                    }
                )
                if created:
                    capital_created += 1
            except (Business.DoesNotExist, BusinessScale.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'    Could not create capital item: {str(e)}'))
        
        # Create risks
        for risk_data in RISKS:
            try:
                business = Business.objects.get(name=risk_data['business_name'])
                scale = BusinessScale.objects.get(
                    business=business, 
                    scale_type=risk_data['scale_type'],
                    year=risk_data.get('year', 2024)
                )
                risk, created = Risk.objects.get_or_create(
                    scale=scale,
                    specific_risk=risk_data['specific_risk'],
                    defaults={
                        'category': risk_data['category'],
                        'likelihood': risk_data['likelihood'],
                        'impact': risk_data['impact'],
                        'mitigation_strategy': risk_data['mitigation_strategy'],
                        'source': default_source
                    }
                )
                if created:
                    risks_created += 1
            except (Business.DoesNotExist, BusinessScale.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'    Could not create risk: {str(e)}'))
        
        # Create feasibility factors
        for factor_data in FEASIBILITY_FACTORS:
            try:
                business = Business.objects.get(name=factor_data['business_name'])
                scale = BusinessScale.objects.get(
                    business=business, 
                    scale_type=factor_data['scale_type'],
                    year=factor_data.get('year', 2024)
                )
                factor, created = FeasibilityFactor.objects.get_or_create(
                    scale=scale,
                    category=factor_data['category'],
                    sub_category=factor_data['sub_category'],
                    defaults={
                        'rating': factor_data['rating'],
                        'notes': factor_data.get('notes', ''),
                        'source': default_source
                    }
                )
                if created:
                    feasibility_created += 1
            except (Business.DoesNotExist, BusinessScale.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'    Could not create feasibility factor: {str(e)}'))
        
        # Create financial metrics
        for metric_data in FINANCIAL_METRICS:
            try:
                business = Business.objects.get(name=metric_data['business_name'])
                scale = BusinessScale.objects.get(
                    business=business, 
                    scale_type=metric_data['scale_type'],
                    year=metric_data.get('year', 2024)
                )
                metric, created = FinancialMetric.objects.get_or_create(
                    scale=scale,
                    source=default_source,
                    defaults={
                        'breakeven_cycles': metric_data['breakeven_cycles'],
                        'gross_margin_pct': metric_data['gross_margin_percent'],
                        'net_margin_pct': metric_data['net_margin_percent'],
                        'roi_pct': metric_data['roi_percent'],
                        'payback_months': metric_data['payback_months'],
                        'is_primary': True
                    }
                )
                if created:
                    financial_created += 1
            except (Business.DoesNotExist, BusinessScale.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'    Could not create financial metric: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Seeded {businesses_created} businesses, {scales_created} scales, '
            f'{capital_created} capital items, {risks_created} risks, '
            f'{feasibility_created} feasibility factors, {financial_created} financial metrics'
        ))

    def seed_operating_costs(self, force=False):
        """Seed operating costs data - UPDATED for new schema"""
        existing_count = OperatingCost.objects.count()
        
        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Operating costs already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            OperatingCost.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing operating costs.'))
        
        created = 0
        default_source = Source.objects.filter(is_primary_source=True).first()
        
        for cost_data in OPERATING_COSTS:
            try:
                business = Business.objects.get(name=cost_data['business_name'])
                scale = BusinessScale.objects.get(
                    business=business, 
                    scale_type=cost_data['scale_type'],
                    year=cost_data['year']
                )
                
                # Create individual cost entries for each category
                for cost_item in cost_data['costs']:
                    operating_cost, created_obj = OperatingCost.objects.get_or_create(
                        scale=scale,
                        period_number=cost_data['period_number'],
                        period_type=cost_data['period_type'],
                        cost_category=cost_item['category'],
                        defaults={
                            'amount_dalasi': cost_item['amount'],
                            'source': default_source
                        }
                    )
                    if created_obj:
                        created += 1
                        
            except (Business.DoesNotExist, BusinessScale.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'    Could not create operating cost: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {created} operating cost entries'))

    def seed_operations_checklists(self, force=False):
        """Seed operations checklists data"""
        existing_count = OperationsChecklist.objects.count()
        
        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Operations checklists already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            OperationsChecklist.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing operations checklists.'))
        
        created = 0
        for checklist_data in OPERATIONS_CHECKLISTS:
            try:
                business = Business.objects.get(name=checklist_data['business_name'])
                checklist, created_obj = OperationsChecklist.objects.get_or_create(
                    business=business,
                    scale_type=checklist_data['scale_type'],
                    task_type=checklist_data['task_type'],
                    task_name=checklist_data['task_name'],
                    defaults={
                        'description': checklist_data.get('description', ''),
                        'time_of_day': checklist_data.get('time_of_day', ''),
                        'responsible': checklist_data.get('responsible', ''),
                        'duration_minutes': checklist_data.get('duration_minutes'),
                        'order': checklist_data.get('order', 0)
                    }
                )
                if created_obj:
                    created += 1
            except Business.DoesNotExist as e:
                self.stdout.write(self.style.WARNING(f'    Could not create operations checklist: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {created} operations checklists'))

    def seed_business_profiles(self, force=False):
        """Seed business profiles data"""
        existing_count = BusinessProfile.objects.count()
        
        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Business profiles already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            BusinessProfile.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing business profiles.'))
        
        profiles_created = 0
        features_created = 0
        testimonials_created = 0
        
        # Create business profiles
        for profile_data in BUSINESS_PROFILES:
            try:
                sector = Sector.objects.get(name=profile_data['sector_name'])
                # Get business type if specified
                business_type = None
                if profile_data.get('business_name'):
                    try:
                        business_type = Business.objects.get(name=profile_data['business_name'])
                    except Business.DoesNotExist:
                        pass
                
                profile, created = BusinessProfile.objects.get_or_create(
                    name=profile_data['name'],
                    defaults={
                        'owner_name': profile_data.get('owner_name', ''),
                        'owner_position': profile_data.get('owner_position', ''),
                        'description': profile_data['description'],
                        'short_description': profile_data.get('short_description', ''),
                        'email': profile_data.get('email', ''),
                        'phone': profile_data.get('phone', ''),
                        'website': profile_data.get('website', ''),
                        'location': profile_data.get('location', ''),
                        'address': profile_data.get('address', ''),
                        'sector': sector,
                        'business_type': business_type,
                        'is_partner': profile_data.get('is_partner', False),
                        'is_verified': profile_data.get('is_verified', False),
                        'is_featured': profile_data.get('is_featured', False),
                        'partner_type': profile_data.get('partner_type', ''),
                        'interview_date': profile_data.get('interview_date'),
                        'interviewed_by': profile_data.get('interviewed_by', 'GAMBIH Research Team'),
                        'status': profile_data.get('status', 'published')
                    }
                )
                if created:
                    profiles_created += 1
            except Sector.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Sector {profile_data["sector_name"]} not found for profile {profile_data["name"]}'))
        
        # Create business profile features
        for feature_data in BUSINESS_PROFILE_FEATURES:
            try:
                profile = BusinessProfile.objects.get(name=feature_data['business_name'])
                feature, created = BusinessProfileFeature.objects.get_or_create(
                    business_profile=profile,
                    title=feature_data['title'],
                    defaults={
                        'description': feature_data['description'],
                        'icon': feature_data.get('icon', ''),
                        'order': feature_data.get('order', 0)
                    }
                )
                if created:
                    features_created += 1
            except BusinessProfile.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Business profile {feature_data["business_name"]} not found for feature'))
        
        # Create business profile testimonials
        for testimonial_data in BUSINESS_PROFILE_TESTIMONIALS:
            try:
                profile = BusinessProfile.objects.get(name=testimonial_data['business_name'])
                testimonial, created = BusinessProfileTestimonial.objects.get_or_create(
                    business_profile=profile,
                    quote=testimonial_data['quote'],
                    defaults={
                        'author_name': testimonial_data['author_name'],
                        'author_position': testimonial_data.get('author_position', ''),
                        'is_featured': testimonial_data.get('is_featured', False),
                        'order': testimonial_data.get('order', 0)
                    }
                )
                if created:
                    testimonials_created += 1
            except BusinessProfile.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Business profile {testimonial_data["business_name"]} not found for testimonial'))
        
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Seeded {profiles_created} business profiles, '
            f'{features_created} features, {testimonials_created} testimonials'
        ))

    def seed_intelligence_snapshots(self, force=False):
        """Seed intelligence snapshots - PRIMARY READ MODEL"""
        existing_count = IntelligenceSnapshot.objects.count()
        
        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Intelligence snapshots already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            IntelligenceSnapshot.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing intelligence snapshots.'))
        
        created = 0
        default_source = Source.objects.filter(is_primary_source=True).first()
        
        for snapshot_data in INTELLIGENCE_SNAPSHOTS:
            try:
                business = Business.objects.get(name=snapshot_data['business_name'])
                
                snapshot, created_obj = IntelligenceSnapshot.objects.get_or_create(
                    business=business,
                    scale_type=snapshot_data['scale_type'],
                    year=snapshot_data['year'],
                    version=snapshot_data.get('version', 1),
                    defaults={
                        'is_latest': snapshot_data.get('is_latest', True),
                        'status': snapshot_data.get('status', 'published'),
                        'data': snapshot_data['data'],
                        'startup_cost': snapshot_data.get('startup_cost'),
                        'gross_margin_pct': snapshot_data.get('gross_margin_pct'),
                        'payback_months': snapshot_data.get('payback_months'),
                        'feasibility_score': snapshot_data.get('feasibility_score'),
                        'risk_score': snapshot_data.get('risk_score'),
                        'min_investment': snapshot_data.get('min_investment'),
                        'max_investment': snapshot_data.get('max_investment'),
                        'summary_text': snapshot_data.get('summary_text', ''),
                        'primary_source': default_source
                    }
                )
                if created_obj:
                    created += 1
            except Business.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Business {snapshot_data["business_name"]} not found for snapshot'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {created} intelligence snapshots'))

    def seed_time_series_metrics(self, force=False):
        """Seed time series metrics for trends"""
        existing_count = TimeSeriesMetric.objects.count()
        
        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Time series metrics already exist ({existing_count} found). Use --force to re-seed.'))
            return
        
        if force and existing_count > 0:
            TimeSeriesMetric.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing time series metrics.'))
        
        created = 0
        
        for metric_data in TIME_SERIES_METRICS:
            try:
                business = Business.objects.get(name=metric_data['business_name'])
                source = Source.objects.filter(name=metric_data['source_name']).first()
                
                if not source:
                    source = Source.objects.filter(is_primary_source=True).first()
                
                metric, created_obj = TimeSeriesMetric.objects.get_or_create(
                    business=business,
                    scale_type=metric_data.get('scale_type'),
                    metric_name=metric_data['metric_name'],
                    year=metric_data['year'],
                    defaults={
                        'value_numeric': metric_data['value_numeric'],
                        'source': source
                    }
                )
                if created_obj:
                    created += 1
            except Business.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Business {metric_data["business_name"]} not found for time series'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {created} time series metrics'))

    def seed_content(self, force=False):
        """Seed content data (articles, videos, tags, comments, case studies)"""
        from apps.core.seed_data.content import (
            ARTICLES, VIDEOS, TAGS, COMMENTS, CASE_STUDIES
        )
        
        # Seed Tags
        tag_objects = {}
        for tag_data in TAGS:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'slug': slugify(tag_data['name'])}
            )
            tag_objects[tag_data['name']] = tag
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {len(tag_objects)} tags'))
        
        # Seed Articles
        articles_created = 0
        for article_data in ARTICLES:
            try:
                sector = Sector.objects.get(name=article_data['sector_name']) if article_data.get('sector_name') else None
                business = Business.objects.get(name=article_data['business_name']) if article_data.get('business_name') else None
                
                published_at = timezone.now() - timedelta(days=article_data.get('published_days_ago', 0))
                
                # Generate unique slug
                base_slug = slugify(article_data['title'])
                slug = base_slug
                counter = 1
                while Article.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                article, created = Article.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': article_data['title'],
                        'excerpt': article_data['excerpt'],
                        'content': article_data['content'],
                        'author': article_data['author'],
                        'read_time': article_data['read_time'],
                        'is_premium': article_data['is_premium'],
                        'is_featured': article_data['is_featured'],
                        'status': article_data['status'],
                        'sector': sector,
                        'business': business,
                        'published_at': published_at
                    }
                )
                if created:
                    articles_created += 1
                    
                    # Add tags to article
                    for tag_name in article_data.get('tag_names', []):
                        if tag_name in tag_objects:
                            ArticleTag.objects.get_or_create(
                                article=article,
                                tag=tag_objects[tag_name]
                            )
            except (Sector.DoesNotExist, Business.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'    Could not create article {article_data["title"]}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {articles_created} articles'))
        
        # Seed Videos
        videos_created = 0
        for video_data in VIDEOS:
            try:
                sector = Sector.objects.get(name=video_data['sector_name']) if video_data.get('sector_name') else None
                business = Business.objects.get(name=video_data['business_name']) if video_data.get('business_name') else None
                
                published_at = timezone.now() - timedelta(days=video_data.get('published_days_ago', 0))
                
                base_slug = slugify(video_data['slug'])
                slug = base_slug
                counter = 1
                while Video.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                video, created = Video.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': video_data['title'],
                        'description': video_data['description'],
                        'platform': video_data['platform'],
                        'platform_video_id': video_data['platform_video_id'],
                        'duration': video_data['duration'],
                        'is_premium': video_data['is_premium'],
                        'is_featured': video_data['is_featured'],
                        'status': video_data['status'],
                        'sector': sector,
                        'business': business,
                        'published_at': published_at
                    }
                )
                if created:
                    videos_created += 1
                    
                    # Add tags to video
                    for tag_name in video_data.get('tag_names', []):
                        if tag_name in tag_objects:
                            VideoTag.objects.get_or_create(
                                video=video,
                                tag=tag_objects[tag_name]
                            )
            except (Sector.DoesNotExist, Business.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'    Could not create video {video_data["title"]}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {videos_created} videos'))
        
        # Seed Comments
        comments_created = 0
        for comment_data in COMMENTS:
            try:
                article = Article.objects.get(title=comment_data['article_title'])
                
                existing_comment = Comment.objects.filter(
                    article=article,
                    user_name=comment_data['user_name'],
                    user_email=comment_data['user_email'],
                    content=comment_data['content']
                ).first()
                
                if not existing_comment:
                    comment = Comment.objects.create(
                        article=article,
                        user_name=comment_data['user_name'],
                        user_email=comment_data['user_email'],
                        content=comment_data['content'],
                        is_approved=comment_data['is_approved']
                    )
                    comments_created += 1
            except Article.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Could not create comment: Article {comment_data["article_title"]} not found'))
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {comments_created} comments'))
        
        # Seed Case Studies
        case_studies_created = 0
        for case_study_data in CASE_STUDIES:
            try:
                sector = Sector.objects.get(name=case_study_data['sector_name'])
                
                published_at = timezone.now() - timedelta(days=case_study_data.get('published_days_ago', 0))
                
                base_slug = slugify(case_study_data['title'])
                slug = base_slug
                counter = 1
                while CaseStudy.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                case_study, created = CaseStudy.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': case_study_data['title'],
                        'excerpt': case_study_data['excerpt'],
                        'content': case_study_data['content'],
                        'business_name': case_study_data['business_name'],
                        'business_type': case_study_data['business_type'],
                        'sector': sector,
                        'initial_investment': case_study_data.get('initial_investment'),
                        'revenue_generated': case_study_data.get('revenue_generated'),
                        'roi_percent': case_study_data.get('roi_percent'),
                        'timeline_months': case_study_data.get('timeline_months'),
                        'is_success': case_study_data['is_success'],
                        'key_lessons': case_study_data['key_lessons'],
                        'author': case_study_data['author'],
                        'is_featured': case_study_data['is_featured'],
                        'status': case_study_data['status'],
                        'published_at': published_at
                    }
                )
                if created:
                    case_studies_created += 1
                    
                    # Add tags to case study
                    for tag_name in case_study_data.get('tag_names', []):
                        if tag_name in tag_objects:
                            CaseStudyTag.objects.get_or_create(
                                case_study=case_study,
                                tag=tag_objects[tag_name]
                            )
            except Sector.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Could not create case study {case_study_data["title"]}: Sector not found'))

        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {case_studies_created} case studies'))

    def seed_countries(self, force=False):
        """Seed countries and regions"""
        from apps.core.models import Country, Region

        existing_count = Country.objects.count()

        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Countries already exist ({existing_count} found). Use --force to re-seed.'))
            return

        if force and existing_count > 0:
            Country.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing countries.'))

        countries_created = 0
        for country_data in COUNTRIES:
            country, created = Country.objects.get_or_create(
                code=country_data['country'],
                defaults={
                    'name': country_data['name'],
                    'flag_emoji': country_data.get('flag_emoji', ''),
                    'currency': country_data.get('currency', 'GMD'),
                    'currency_symbol': country_data.get('currency_symbol', ''),
                    'population': country_data.get('population'),
                    'gdp_per_capita_usd': country_data.get('gdp_per_capita'),
                    'is_active': country_data.get('is_active', True),
                    'order': country_data.get('order', 0),
                }
            )
            if created:
                countries_created += 1

        regions_created = 0
        for region_data in REGIONS:
            region, created = Region.objects.get_or_create(
                slug=region_data['slug'],
                defaults={
                    'name': region_data['name'],
                    'description': region_data.get('description', ''),
                }
            )
            if created:
                regions_created += 1
            for code in region_data.get('countries', []):
                try:
                    country = Country.objects.get(code=code)
                    region.countries.add(country)
                except Country.DoesNotExist:
                    pass

        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {countries_created} countries, {regions_created} regions'))

    def seed_sector_stats(self, force=False):
        """Seed sector statistics"""
        from apps.sectors.models import SectorStat

        existing_count = SectorStat.objects.count()

        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Sector stats already exist ({existing_count} found). Use --force to re-seed.'))
            return

        if force and existing_count > 0:
            SectorStat.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing sector stats.'))

        created = 0
        default_source = Source.objects.filter(is_primary_source=True).first()

        for stat_data in SECTOR_STATS:
            try:
                sector = Sector.objects.get(name=stat_data['sector_name'])
                stat, created_obj = SectorStat.objects.get_or_create(
                    sector=sector,
                    label=stat_data['label'],
                    year=stat_data['year'],
                    defaults={
                        'value': stat_data['value'],
                        'unit': stat_data['unit'],
                        'is_headline': stat_data['is_headline'],
                        'display_order': stat_data['display_order'],
                        'source': default_source,
                    }
                )
                if created_obj:
                    created += 1
            except Sector.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Sector {stat_data["sector_name"]} not found for stat {stat_data["label"]}'))

        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {created} sector stats'))

    def seed_reports(self, force=False):
        """Seed reports"""
        from apps.reports.models import Report

        existing_count = Report.objects.count()

        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Reports already exist ({existing_count} found). Use --force to re-seed.'))
            return

        if force and existing_count > 0:
            Report.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing reports.'))

        created = 0
        for report_data in REPORTS:
            try:
                sector = Sector.objects.get(name=report_data['sector_name']) if report_data.get('sector_name') else None
                business = None
                if report_data.get('business_name'):
                    try:
                        business = Business.objects.get(name=report_data['business_name'])
                    except Business.DoesNotExist:
                        pass

                report, created_obj = Report.objects.get_or_create(
                    title=report_data['title'],
                    defaults={
                        'subtitle': report_data.get('subtitle', ''),
                        'short_description': report_data.get('short_description', ''),
                        'description': report_data.get('description', ''),
                        'report_type': report_data.get('report_type', 'business'),
                        'format': report_data.get('format', 'pdf'),
                        'price': report_data.get('price', 0),
                        'is_free': report_data.get('is_free', False),
                        'is_featured': report_data.get('is_featured', False),
                        'is_bestseller': report_data.get('is_bestseller', False),
                        'page_count': report_data.get('page_count'),
                        'version': report_data.get('version', '1.0'),
                        'author': report_data.get('author', ''),
                        'sector': sector,
                        'business': business,
                        'status': report_data.get('status', 'published'),
                    }
                )
                if created_obj:
                    created += 1
            except Sector.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'    Sector {report_data["sector_name"]} not found for report {report_data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {created} reports'))

    def seed_report_bundles(self, force=False):
        """Seed report bundles"""
        from apps.reports.models import Report, ReportBundle

        existing_count = ReportBundle.objects.count()

        if existing_count > 0 and not force:
            self.stdout.write(self.style.WARNING(f'  Report bundles already exist ({existing_count} found). Use --force to re-seed.'))
            return

        if force and existing_count > 0:
            ReportBundle.objects.all().delete()
            self.stdout.write(self.style.WARNING('  Cleared existing report bundles.'))

        created = 0
        for bundle_data in REPORT_BUNDLES:
            bundle, created_obj = ReportBundle.objects.get_or_create(
                slug=bundle_data['slug'],
                defaults={
                    'name': bundle_data['name'],
                    'description': bundle_data.get('description', ''),
                    'price': bundle_data['price'],
                    'original_price': bundle_data['original_price'],
                    'is_featured': bundle_data.get('is_featured', False),
                    'status': bundle_data.get('status', 'published'),
                }
            )
            if created_obj:
                created += 1
            for title in bundle_data.get('report_titles', []):
                try:
                    report = Report.objects.get(title=title)
                    bundle.reports.add(report)
                except Report.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'    Report "{title}" not found for bundle {bundle_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'  ✓ Seeded {created} report bundles'))
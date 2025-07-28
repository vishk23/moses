"""
R360 Package - Relationship 360 Customer Grouping System

Provides three key types for customer analysis:
- portfolio_key: Groups by address OR ownership (full relationship view)
- address_key: Groups by address only (household view)
- ownership_key: Groups by ownership only (business relationship view)

Usage:
    import src.r360
    
    # Generate all keys
    portfolio_data = src.r360.portfolio_key()
    address_data = src.r360.address_key() 
    ownership_data = src.r360.ownership_key()
"""

import src.r360.core

def portfolio_key(save_to_db=True):
    """Generate portfolio key (groups by address OR ownership)"""
    return src.r360.core.generate_portfolio_key(save_to_db=save_to_db)

def address_key(save_to_db=True):
    """Generate address key (groups by address only)"""
    return src.r360.core.generate_address_key(save_to_db=save_to_db)

def ownership_key(save_to_db=True):
    """Generate ownership key (groups by ownership only)"""
    return src.r360.core.generate_ownership_key(save_to_db=save_to_db)

"""file : test_links.py

Test if links of shops is working
"""

import pytest
import requests
import numpy as np

# # Fonctions scrapping
from operators.extract_data import get_shop_links

# Fonctions db
from helpers.connect import connect_db_sqlalchemy


@pytest.fixture
def lst_links():
    """Get random links from each shop

    Returns:
        list: list of links
    """
    conn = connect_db_sqlalchemy()
    df = get_shop_links(conn)

    # get one link for each shop, randomly
    df["link"] = df["links"].apply(lambda x: np.random.choice(x))
    return df["link"].to_list()


def test_links(lst_links: list):
    """Test if links of shops is working

    Args:
        lst_links (list): list of links
    """
    for link in lst_links:
        print(link)
        assert requests.get(link).status_code == 200, f"Link {link} is not working"

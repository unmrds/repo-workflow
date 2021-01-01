import config
import repositories
import time

collection_root = "http://digitalrepository.unm.edu/"

# ETDs
publications = [
    #"amst_etds",
    #"anderson_etds",
    #"anth_etds",
    "arch_etds",
    "arth_etds",
    "biol_etds",
    "biom_etds",
    "chem_etds",
    "cj_etds",
    "dehy_etds",
    "eps_etds",
    "econ_etds",
    "educ_hess_etds",
    "educ_ifce_etds",
    "educ_llss_etds",
    "educ_spcd_etds",
    "educ_teelp_etds",
    "bme_etds",
    "cbe_etds",
    "ce_etds",
    "cs_etds",
    "ece_etds",
    "me_etds",
    "nsms_etds",
    "ne_etds",
    "ose_etds",
    "engl_etds",
    "fll_etds",
    "geog_etds",
    "hist_etds",
    "ltam_etds",
    "ling_etds",
    "math_etds",
    "msst_etds",
    "mus_etds",
    "nurs_etds",
    "octh_etds",
    "oils_etds",
    "phrm_etds",
    "phil_etds",
    "phyc_etds",
    "pols_etds",
    "psy_etds",
    "padm_etds",
    "soc_etds",
    "span_etds",
    "shs_etds",
    "thea_etds"
]

for publication in publications:
    collection_parent = collection_root + publication
    attempts = 0
    while attempts < 5:
        try:
            dc_test = repositories.DigitalCommons(publication=publication, process = "production")
            dc_test.query(
                metadata_field=("parent_link", collection_parent),
                limit=1000,
            )
            print(dc_test.create_dois())
            break
        except:
            print("Request failed. Trying again in 5 seconds. Attempt number: " + str(attempts))
            time.sleep(5)
            attempts += 1


publications = [
    "energizenm"
]

for publication in publications:
    collection_parent = collection_root + publication
    attempts = 0
    while attempts < 5:
        try:
            dc_test = repositories.DigitalCommons(publication=publication, process = "production")
            dc_test.query(
                metadata_field=("parent_link", collection_parent),
                limit=1000,
            )
            print(dc_test.create_dois())
            break
        except:
            print("Request failed. Trying again in 5 seconds. ")
            time.sleep(5)
            attempts += 1

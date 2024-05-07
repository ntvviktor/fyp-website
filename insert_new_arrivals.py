from sqlalchemy import create_engine
from webapp.models.book_model import NewArrival
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
try:
    session.add_all([NewArrival("1847941834", "Atomic Habits: The life-changing million copy bestseller",
                                17.90, "James Clear", "https://m.media-amazon.com/images/I/81Ls+SBCLiL._SY522_.jpg",
                                "Transform your life with tiny changes in behaviour, starting now. People think that when you want to change your life, you need to think big. But world-renowned habits expert James Clear has discovered another way. He knows that real change comes from the compound effect of hundreds of small decisions: doing two push-ups a day, waking up five minutes early, or holding a single short phone call.",
                                "https://www.amazon.sg/Atomic-Habits-life-changing-million-bestseller/dp/1847941834/ref=sr_1_5?crid=33VUES08O8X2P&dib=eyJ2IjoiMSJ9.NA3IaySr3XT_6gW0EUppcfEEnZXFvd7GmcMj9gtnWBfmMVc5QBF5miOJohM9xLD0Guvo7mPfkCtoEQ8EmwitjAxOhgdEcHEBZHSEVRwmynzrmJRomEZEmsWWuQep0j0NCEuVbxu9J9ezDOFS0Ye03PEZb-2k6C3_zP-wVpMQtR5bstWaZTf5ALz9SQoOowZVeFdPWd2DmdDdjvQeraZD4Ml-nVzFpPcF11lxnxcccHk5gzGEd_oshO3_dEdFGUgcTKRtSDqgQ1aJNjs_bQFc-7EpMIIJBzDA2QZrRMdxzcU.bJf2fGSFIx5SsdfpYif5LY1uat2RenuZgTRD0Bjoo44&dib_tag=se&keywords=books&qid=1714999609&sprefix=%2Caps%2C297&sr=8-5", 2018),
                     NewArrival("1544512279", "Can't Hurt Me: Master Your Mind and Defy the Odds",
                                32.84, "David Goggins", "https://m.media-amazon.com/images/I/61pDNU9qEGL._SY522_.jpg",
                                "In Can't Hurt Me, he shares his astonishing life story and reveals that most of us tap into only 40% of our capabilities. Goggins calls this The 40% Rule, and his story illuminates a path that anyone can follow to push past pain, demolish fear, and reach their full potential.",
                                "https://www.amazon.sg/Cant-Hurt-Me-Master-Your/dp/1544512279/ref=pd_sbs_d_sccl_4_24/358-1005122-6131925?pd_rd_w=OqmwJ&content-id=amzn1.sym.3cdd08be-a5f7-4ba6-af25-e5fb2bb96dba&pf_rd_p=3cdd08be-a5f7-4ba6-af25-e5fb2bb96dba&pf_rd_r=CRPVYWXCQSP11Z3T9SV3&pd_rd_wg=AVRyd&pd_rd_r=e90241ab-db11-4783-bf6d-2a60b0ffdb28&pd_rd_i=1544512279&psc=1", 2018),
                     NewArrival("8579327079", "Read People Like a Book: How to Analyze, Understand, and Predict People’s Emotions, Thoughts, Intentions, and Behaviors (How to be More Likable and Charismatic)",
                                19.79, "Patrick King", "https://m.media-amazon.com/images/I/61BqxChoN2L._SY522_.jpg",
                                "Speed read people, decipher body language, detect lies, and understand human nature. Is it possible to analyze people without them saying a word? Yes, it is. Learn how to become a “mind reader” and forge deep connections.",
                                "https://www.amazon.sg/Read-People-Like-Book-Charismatic/dp/B08QBB3MTG/ref=sr_1_48?crid=7FY4ZFZ4G8FH&dib=eyJ2IjoiMSJ9.NA3IaySr3XT_6gW0EUppcfEEnZXFvd7GmcMj9gtnWBfmMVc5QBF5miOJohM9xLD0Guvo7mPfkCtoEQ8EmwitjAxOhgdEcHEBZHSEVRwmynzrmJRomEZEmsWWuQep0j0NCEuVbxu9J9ezDOFS0Ye03PEZb-2k6C3_zP-wVpMQtR5bstWaZTf5ALz9SQoOowZVeFdPWd2DmdDdjvQeraZD4Ml-nVzFpPcF11lxnxcccHk5gzGEd_oshO3_dEdFGUgcTKRtSDqgQ1aJNjs_bQFc-7EpMIIJBzDA2QZrRMdxzcU.bJf2fGSFIx5SsdfpYif5LY1uat2RenuZgTRD0Bjoo44&dib_tag=se&keywords=books&qid=1715000266&sprefix=books%2Caps%2C254&sr=8-48", 2022),
                     NewArrival("979-8737886295", "Dark Psychology and Manipulation: Discover 40 Covert Emotional Manipulation Techniques, Mind Control",
                                42.66, "William Cooper", "https://m.media-amazon.com/images/I/616Rz77u87L._SY522_.jpg", "Knowing these techniques is certainly important!",
                                "https://www.amazon.sg/Dark-Psychology-Manipulation-Techniques-Brainwashing/dp/B092HLG4J1/ref=srd_d_ssims_T2_d_sccl_2_2/358-1005122-6131925?pd_rd_w=EPTm9&content-id=amzn1.sym.96d86cc4-eb9c-4bc9-a575-efa11e41478d&pf_rd_p=96d86cc4-eb9c-4bc9-a575-efa11e41478d&pf_rd_r=PSSJHBKNDMA1B8SQ17XN&pd_rd_wg=aFxx8&pd_rd_r=92884ae6-38fe-4301-8808-8d57351fe6b3&pd_rd_i=B092HLG4J1&psc=1",2021),
                     NewArrival("0345816021", "12 Rules for Life: An Antidote to Chaos", 24.67,
                                "Jordan B. Peterson", "https://m.media-amazon.com/images/I/61BRxtp9qtL._SY522_.jpg",
                                "Humorous, surprising and informative, Dr. Peterson tells us why skateboarding boys and girls must be left alone, what terrible fate awaits those who criticize too easily, and why you should always pet a cat when you meet one on the street.",
                                "https://www.amazon.sg/12-Rules-Life-Antidote-Chaos/dp/0345816021/ref=sr_1_1?crid=3CL5DQXA88WY7&dib=eyJ2IjoiMSJ9.A9iQGugc9HbvwfPRfi6zcPVUkKowrbjCIqZh7i8oOAtsjBwzeIC46kIDNHJzCROtrerf4eZwVGR0NFHLdAroexOIWqsGNw7ol-wylROsJuu1sCHA7IS8yF0Dh9PI0m_ed782AZgsOHweyp-xl6zcFC_KHee5KIoQOcpo6c0CXTBOX51jz4KKrERJoJR8FEw60_yp8jF4QoKJtrXDMK5pToa_jGda6mAaKgvHrku1tGTIGOF_w8ysvXW-B78jnapPIS3kELM8PKRLHQT_HSvY-8K1Vs0bQPniH6kJj3kLnsk.yF9hbeh3HAP65Vq7FxljaVM19IeCkNKn1KzjEABB94w&dib_tag=se&keywords=jordan+peterson&qid=1715000652&sprefix=Jordan+P%2Caps%2C318&sr=8-1", 2018)
                     ])
    session.commit()
except IntegrityError as e:
    session.rollback()
    print(f"Skipped duplicate book due to {e}")
finally:
    session.close()

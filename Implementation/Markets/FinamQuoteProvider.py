# this class serves the same function as MoexQuoteProvider and should return
# identical results, however there is a problem that must be solved -
# dictionary of stocks with unique Finam id numbers (those are required for
# quote download) is now stored within the class and needs to be renewed
# periodically

import io
import numpy
import pandas
import requests

from datetime import date
from typing import List

from urllib.parse import urlencode
from Products.QuoteProvider import QuoteProvider


class FinamQuoteProvider(QuoteProvider):
    def __init__(self, boardId: str):
        self.__boardId = boardId

    def getQuotes(
        self,
        ticker: str,
        observationDates: List[date]
    ) -> List[float]:
        startDate = min(observationDates)
        endDate = max(observationDates)
        resultDates = pandas.DataFrame(observationDates)
        resultDates.columns = ['TRADEDATE']
        resultDates['TRADEDATE'] = pandas.to_datetime(
            resultDates['TRADEDATE']
        )

        # every instrument in Finam has its own numeric id, but the dictionary
        # may be outdated, so if this class should be used that problem bust
        # be resolved
        finamIdStorage = {
            'OZON': 2179435,
            'ABRD': 82460,
            'AESL': 181867,
            'AFKS': 19715,
            'AFLT': 29,
            'AGRO': 399716,
            'AKRN': 17564,
            'ALBK': 82616,
            'ALNU': 81882,
            'ALRS': 81820,
            'AMEZ': 20702,
            'APTK': 13855,
            'AQUA': 35238,
            'ARMD': 19676,
            'ARSA': 19915,
            'ASSB': 16452,
            'AVAN': 82843,
            'AVAZ': 39,
            'AVAZP': 40,
            'BANE': 81757,
            'BANEP': 81758,
            'BGDE': 175840,
            'BISV': 35242,
            'BISVP': 35243,
            'BLNG': 21078,
            'BRZL': 81901,
            'BSPB': 20066,
            'CBOM': 420694,
            'CHEP': 20999,
            'CHGZ': 81933,
            'CHKZ': 21000,
            'CHMF': 16136,
            'CHMK': 21001,
            'CHZN': 19960,
            'CLSB': 16712,
            'CLSBP': 16713,
            'CNTL': 21002,
            'CNTLP': 81575,
            'DASB': 16825,
            'DGBZ': 17919,
            'DIOD': 35363,
            'DIXY': 18564,
            'DVEC': 19724,
            'DZRD': 74744,
            'DZRDP': 74745,
            'ELTZ': 81934,
            'ENRU': 16440,
            'EPLN': 451471,
            'ERCO': 81935,
            'FEES': 20509,
            'FESH': 20708,
            'FORTP': 82164,
            'GAZA': 81997,
            'GAZAP': 81998,
            'GAZC': 81398,
            'GAZP': 16842,
            'GAZS': 81399,
            'GAZT': 82115,
            'GCHE': 20125,
            'GMKN': 795,
            'GRAZ': 16610,
            'GRNT': 449114,
            'GTLC': 152876,
            'GTPR': 175842,
            'GTSS': 436120,
            'HALS': 17698,
            'HIMC': 81939,
            'HIMCP': 81940,
            'HYDR': 20266,
            'IDJT': 388276,
            'IDVP': 409486,
            'IGST': 81885,
            'IGST03': 81886,
            'IGSTP': 81887,
            'IRAO': 20516,
            'IRGZ': 9,
            'IRKT': 15547,
            'ISKJ': 17137,
            'JNOS': 15722,
            'JNOSP': 15723,
            'KAZT': 81941,
            'KAZTP': 81942,
            'KBSB': 19916,
            'KBTK': 35285,
            'KCHE': 20030,
            'KCHEP': 20498,
            'KGKC': 83261,
            'KGKCP': 152350,
            'KLSB': 16329,
            'KMAZ': 15544,
            'KMEZ': 22525,
            'KMTZ': 81903,
            'KOGK': 20710,
            'KRKN': 81891,
            'KRKNP': 81892,
            'KRKO': 81905,
            'KRKOP': 81906,
            'KROT': 510,
            'KROTP': 511,
            'KRSB': 20912,
            'KRSBP': 20913,
            'KRSG': 15518,
            'KSGR': 75094,
            'KTSB': 16284,
            'KTSBP': 16285,
            'KUBE': 522,
            'KUNF': 81943,
            'KUZB': 83165,
            'KZMS': 17359,
            'KZOS': 81856,
            'KZOSP': 81857,
            'LIFE': 74584,
            'LKOH': 8,
            'LNTA': 385792,
            'LNZL': 21004,
            'LNZLP': 22094,
            'LPSB': 16276,
            'LSNG': 31,
            'LSNGP': 542,
            'LSRG': 19736,
            'LVHK': 152517,
            'MAGE': 74562,
            'MAGEP': 74563,
            'MAGN': 16782,
            'MERF': 20947,
            'MFGS': 30,
            'MFGSP': 51,
            'MFON': 152516,
            'MGNT': 17086,
            'MGNZ': 20892,
            'MGTS': 12984,
            'MGTSP': 12983,
            'MGVM': 81829,
            'MISB': 16330,
            'MISBP': 16331,
            'MNFD': 80390,
            'MOBB': 82890,
            'MOEX': 152798,
            'MORI': 81944,
            'MOTZ': 21116,
            'MRKC': 20235,
            'MRKK': 20412,
            'MRKP': 20107,
            'MRKS': 20346,
            'MRKU': 20402,
            'MRKV': 20286,
            'MRKY': 20681,
            'MRKZ': 20309,
            'MRSB': 16359,
            'MSNG': 6,
            'MSRS': 16917,
            'MSST': 152676,
            'MSTT': 74549,
            'MTLR': 21018,
            'MTLRP': 80745,
            'MTSS': 15523,
            'MUGS': 81945,
            'MUGSP': 81946,
            'MVID': 19737,
            'NAUK': 81992,
            'NFAZ': 81287,
            'NKHP': 450432,
            'NKNC': 20100,
            'NKNCP': 20101,
            'NKSH': 81947,
            'NLMK': 17046,
            'NMTP': 19629,
            'NNSB': 16615,
            'NNSBP': 16616,
            'NPOF': 81858,
            'NSVZ': 81929,
            'NVTK': 17370,
            'ODVA': 20737,
            'OFCB': 80728,
            'OGKB': 18684,
            'OMSH': 22891,
            'OMZZP': 15844,
            'OPIN': 20711,
            'OSMP': 21006,
            'OTCP': 407627,
            'PAZA': 81896,
            'PHOR': 81114,
            'PHST': 19717,
            'PIKK': 18654,
            'PLSM': 81241,
            'PLZL': 17123,
            'PMSB': 16908,
            'PMSBP': 16909,
            'POLY': 175924,
            'PRFN': 83121,
            'PRIM': 17850,
            'PRIN': 22806,
            'PRMB': 80818,
            'PRTK': 35247,
            'PSBR': 152320,
            'QIWI': 181610,
            'RASP': 17713,
            'RBCM': 74779,
            'RDRB': 181755,
            'RGSS': 181934,
            'RKKE': 20321,
            'RLMN': 152677,
            'RLMNP': 388313,
            'RNAV': 66644,
            'RODNP': 66693,
            'ROLO': 181316,
            'ROSB': 16866,
            'ROSN': 17273,
            'ROST': 20637,
            'RSTI': 20971,
            'RSTIP': 20972,
            'RTGZ': 152397,
            'RTKM': 7,
            'RTKMP': 15,
            'RTSB': 16783,
            'RTSBP': 16784,
            'RUAL': 414279,
            'RUALR': 74718,
            'RUGR': 66893,
            'RUSI': 81786,
            'RUSP': 20712,
            'RZSB': 16455,
            'SAGO': 445,
            'SAGOP': 70,
            'SARE': 11,
            'SAREP': 24,
            'SBER': 3,
            'SBERP': 23,
            'SELG': 81360,
            'SELGP': 82610,
            'SELL': 21166,
            'SIBG': 436091,
            'SIBN': 2,
            'SKYC': 83122,
            'SNGS': 4,
            'SNGSP': 13,
            'STSB': 20087,
            'STSBP': 20088,
            'SVAV': 16080,
            'SYNG': 19651,
            'SZPR': 22401,
            'TAER': 80593,
            'TANL': 81914,
            'TANLP': 81915,
            'TASB': 16265,
            'TASBP': 16266,
            'TATN': 825,
            'TATNP': 826,
            'TGKA': 18382,
            'TGKB': 17597,
            'TGKBP': 18189,
            'TGKD': 18310,
            'TGKDP': 18391,
            'TGKN': 18176,
            'TGKO': 81899,
            'TNSE': 420644,
            'TORS': 16797,
            'TORSP': 16798,
            'TRCN': 74561,
            'TRMK': 18441,
            'TRNFP': 1012,
            'TTLK': 18371,
            'TUCH': 74746,
            'TUZA': 20716,
            'UCSS': 175781,
            'UKUZ': 20717,
            'UNAC': 22843,
            'UNKL': 82493,
            'UPRO': 18584,
            'URFD': 75124,
            'URKA': 19623,
            'URKZ': 82611,
            'USBN': 81953,
            'UTAR': 15522,
            'UTII': 81040,
            'UTSY': 419504,
            'UWGN': 414560,
            'VDSB': 16352,
            'VGSB': 16456,
            'VGSBP': 16457,
            'VJGZ': 81954,
            'VJGZP': 81955,
            'VLHZ': 17257,
            'VRAO': 20958,
            'VRAOP': 20959,
            'VRSB': 16546,
            'VRSBP': 16547,
            'VSMO': 15965,
            'VSYD': 83251,
            'VSYDP': 83252,
            'VTBR': 19043,
            'VTGK': 19632,
            'VTRS': 82886,
            'VZRZ': 17068,
            'VZRZP': 17067,
            'WTCM': 19095,
            'WTCMP': 19096,
            'YAKG': 81917,
            'YKEN': 81766,
            'YKENP': 81769,
            'YNDX': 388383,
            'YRSB': 16342,
            'YRSBP': 16343,
            'ZHIV': 181674,
            'ZILL': 81918,
            'ZMZN': 556,
            'ZMZNP': 603,
            'ZVEZ': 82001
        }
        finamUrl = "http://export.finam.ru/"
        # identifies the market (shares, bonds, currency etc.),
        # for shares any number works
        market = 0
        periods = {
            'tick': 1,
            'min': 2,
            '5min': 3,
            '10min': 4,
            '15min': 5,
            '30min': 6,
            'hour': 7,
            'daily': 8,
            'week': 9,
            'month': 10
        }
        # daily quotes
        quotePeriod = 8

        linkParams = urlencode(
            [
                # market
                ('market', market),
                # finam id for the instrument taken from the list "tickers"
                ('em', finamIdStorage[ticker]),
                ('code', ticker),
                # unidentified parameter
                ('apply', 0),
                # day number for the start date (1-31)
                ('df', startDate.day),
                # month number for the start date (0-11)
                ('mf', startDate.month - 1),
                ('yf', startDate.year),
                ('from', startDate),
                ('dt', endDate.day),
                ('mt', endDate.month - 1),
                ('yt', endDate.year),
                ('to', endDate),
                ('p', quotePeriod),
                # filename
                ('f', ticker + "_" + startDate.strftime(
                    '%Y%m%d'
                ) + "_" + endDate.strftime('%Y%m%d')),
                # file extension
                ('e', ".csv"),
                ('cn', ticker),
                # date format, for more info -
                # https://www.finam.ru/profile/moex-akcii/sberbank/export/
                ('dtf', 1),
                # time format
                ('tmf', 1),
                # candle (0 - open; 1 - close)
                ('MSOR', 0),
                # Moscow time
                ('mstime', "on"),
                # correction for timezone
                ('mstimever', 1),
                # fields separator (1 - ",", 2 - ".", 3 - ";", 4 - "tab",
                # 5 - "space")
                ('sep', 1),
                # digits separator
                ('sep2', 1),
                # data format (6 possible choices)
                ('datf', 1),
                # column headers
                ('at', 1)]
        )
        # forming the url link of csv file
        # based on outlined parameters and inputs (dates & ticker)
        urlLink = finamUrl + ticker + "_" + startDate.strftime(
            '%Y%m%d'
        ) + "_" + endDate.strftime('%Y%m%d') + ".csv?" + linkParams
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'
        }
        result = requests.get(urlLink, headers=headers)
        quoteData = pandas.read_csv(io.StringIO(result.text))
        quoteData.drop(
            ['<TICKER>',
                '<PER>',
                '<TIME>',
                '<OPEN>',
                '<HIGH>',
                '<LOW>',
                '<VOL>'],
            axis=1,
            inplace=True
        )
        quoteData.rename(
            columns={
                "<DATE>": "TRADEDATE",
                "<CLOSE>": "CLOSE"
            },
            inplace=True
        )
        quoteData.set_index('TRADEDATE', inplace=True)
        quoteData.index = pandas.to_datetime(quoteData.index, format='%Y%m%d')
        result = resultDates.merge(
            right=quoteData,
            how='left',
            on='TRADEDATE',
        )
        result['CLOSE'].replace({numpy.NAN: None}, inplace=True)
        return result['CLOSE'].tolist()


# this simple example checks if objects of MoexQuoteProvider
# and FinamQuoteProvider return identical results for a set of
# 5 tickers and 5 dates
if __name__ == '__main__':
    from Markets.MoexQuoteProvider import MoexQuoteProvider

    sampleTickers = [
        'GAZP',
        'SBER',
        'MOEX',
        'CHMF',
        'ALRS'
    ]
    sampleDates = [
        date(2021, 1, 11),
        date(2022, 1, 9),
        date(2022, 2, 10),
        date(2022, 10, 3),
        date(2022, 10, 10)
    ]
    sampleFinamObject = FinamQuoteProvider('TQBR')
    sampleMoexObject = MoexQuoteProvider('TQBR')
    for stock in sampleTickers:
        print(
            sampleFinamObject.getQuotes(
                stock,
                sampleDates
            ) == sampleMoexObject.getQuotes(stock, sampleDates)
        )

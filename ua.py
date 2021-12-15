# !/usr/bin/python 
# -*- coding: utf-8 -*-

# filePath: Do not edit
# Author: Derek.S(derekseli@outlook.com)
# Date: 2020-11-25 07:49:18
# LastEditors: Derek.S(derekseli@outlook.com)
# LastEditTime: 2021-12-15 11:10:50

import random
import string

osVer = {
    "Windows": [
        "10.0",
        "6.3",
        "6.2",
        "6.1"],
    "OSX": [
        "10.15",
        "10.15.1",
        "10.15.2",
        "10.15.3",
        "10.15.4",
        "10.15.5",
        "10.15.6",
        "10.15.7",
        "11.0"
        ]
}
browserVer = {
    "Chrome": [
        "87",
        "96"
    ],
    "Firefox": [
        "90",
        "95"
    ],
    "Edge": [
        "87",
        "96"
    ]
}

# random Windows Version
def random_Windows_Ver():
    return random.choice(osVer["Windows"])

# random Mac Version
def random_Mac_Ver():
    return random.choice(osVer["OSX"])

# random Chrome Version
def random_Chrome_Ver():
    config_Ver_range_low = int(browserVer["Chrome"][0])
    config_Ver_range_high = int(browserVer["Chrome"][1])
    rand_Ver = '{0}.{1}.{2}.{3}'.format(
        random.randint(config_Ver_range_low, config_Ver_range_high),
        0,
        random.randint(1000, 5000),
        random.randint(10, 99)
    )
    return rand_Ver

# random Webkit/Safari Version
def random_WebkitVer():
    rand_Ver = '{0}.{1}'.format(
        random.randint(400, 999),
        random.randint(0, 99)
    )
    return rand_Ver

# random Firefox Version
def random_Firefox_Ver():
    config_Ver_range_low = int(browserVer["Firefox"][0])
    config_Ver_range_high = int(browserVer["Firefox"][1])
    rand_Ver = '{}.0'.format(random.randint(
        config_Ver_range_low, config_Ver_range_high
    ))
    return rand_Ver

# random Edge Version
def random_Edge_Ver():
    config_Ver_range_low = int(browserVer["Edge"][0])
    config_Ver_range_high = int(browserVer["Edge"][1])
    rand_Ver = '{0}.{1}.{2}.{3}'.format(
        random.randint(config_Ver_range_low, config_Ver_range_high),
        0,
        random.randint(400, 900),
        random.randint(30, 99)
    )
    return rand_Ver

class UAMaker():
    def chrome_pc_windows(self):
        ua_string = "Mozilla/5.0 (Windows NT {WinVer}; Win64; x64) " \
                    "AppleWebKit/{WebkitVer} (KHTML, like Gecko) " \
                    "Chrome/{ChromeVer} " \
                    "Safari/{WebkitVer}"
        return ua_string.format(
            **{"WinVer": random_Windows_Ver(), "WebkitVer": random_WebkitVer(), "ChromeVer": random_Chrome_Ver()}
        )

    def chrome_pc_linux(self):
        ua_string = "Mozilla/5.0 (X11; Linux x86_64) " \
                    "AppleWebKit/{WebkitVer} (KHTML, like Gecko) " \
                    "Chrome/{ChromeVer} " \
                    "Safari/{WebkitVer}"
        return ua_string.format(
            **{"ChromeVer": random_Chrome_Ver(), "WebkitVer": random_WebkitVer()}
        )

    def chrome_mac(self):
        ua_string = "Mozilla/5.0 (Macintosh; Intel Mac OS X {MacVer}) " \
                    "AppleWebKit/{WebkitVer} (KHTML, like Gecko) " \
                    "Chrome/{ChromeVer} " \
                    "Safari/{WebkitVer}"
        return ua_string.format(
            **{
                "MacVer": random_Mac_Ver(),
                "ChromeVer": random_Chrome_Ver(),
                "WebkitVer": random_WebkitVer()}
        )
    
    def internet_explorer(self):
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv 11.0) like Gecko',
            'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)'
        ]
        rand_UA_String = random.choice(ua_list)
        return rand_UA_String

    def firefox_pc_windows(self):
        ua_string = "Mozilla/5.0 (Windows NT {WinVer}; WOW64; rv:{FirefoxVer}) Gecko/20100101 Firefox/{FirefoxVer}"
        return ua_string.format(
            **{"WinVer": random_Windows_Ver(), "FirefoxVer": random_Firefox_Ver()}
        )

    def firefox_pc_linux(self):
        ua_string = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{FirefoxVer}) Gecko/20100101 Firefox/{FirefoxVer}"
        return ua_string.format(
            **{"FirefoxVer": random_Firefox_Ver()}
        )

    def firefox_mac(self):
        ua_string = "Mozilla/5.0 (Macintosh; Intel Mac OS X {MacVer}; rv:{FirefoxVer}) Gecko/20100101 Firefox/{FirefoxVer}"
        return ua_string.format(
            **{"MacVer": random_Mac_Ver(), "FirefoxVer": random_Firefox_Ver()}
        )

    def safari_mac(self):
        ua_string = "Mozilla/5.0 (Macintosh; Intel Mac OS X {MacVer} " \
                    "AppleWebKit/{WebkitVer} (KHTML, like Gecko) " \
                    "Version/{SafariVer} Safari/{WebkitVer}"
        return ua_string.format(
            **{
                "MacVer": random_Mac_Ver(),
                "WebkitVer": random_WebkitVer(),
                "SafariVer": '{0}.{1}'.format(
                    random.randint(10, 11),
                    random.randint(0, 9)
                )
            }
        )
    
    def edge_pc_windows(self):
        ua_string = "Mozilla/5.0 (Windows NT {WinVer}; Win64; x64) " \
                    "AppleWebKit/{WebkitVer} (KHTML, like Gecko) " \
                    "Chrome/{ChromeVer} " \
                    "Safari/{WebkitVer}" \
                    "Edg/{EdgeVer}"
        return ua_string.format(
            **{"WinVer": random_Windows_Ver(), "WebkitVer": random_WebkitVer(), "ChromeVer": random_Chrome_Ver(), "EdgeVer": random_Edge_Ver()}
        )



    def pc_Windows(self):
        ua = random.choice([
            self.chrome_pc_windows(),
            self.firefox_pc_windows(),
            self.internet_explorer(),
            self.edge_pc_windows()
            ])
        return ua

    def pc_Linux(self):
        ua = random.choice([
            self.chrome_pc_linux(),
            self.firefox_pc_linux()
        ])
        return ua

    def pc_mac(self):
        ua = random.choice([
            self.chrome_mac(),
            self.firefox_mac(),
            self.safari_mac()
        ])
        return ua
    
    def random_PC(self):
        ua = random.choice([
            self.pc_Linux(),
            self.pc_mac(),
            self.pc_Windows()
        ])
        return ua
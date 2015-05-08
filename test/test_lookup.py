import unittest

import sys, os
sys.path.append(os.path.abspath(os.path.join('src', 'plugins')))
import lookup

class TestLookup(unittest.TestCase):
    def test_wiki_formatting(self):
        p = lookup.Lookup(None)
        result = p.deugly_wikimedia(WIKI_TEST)
        self.assertEqual(result, 'THIS IS A TEST with links and other links. And here is the second line.')
        
WIKI_TEST = """{{Infobox film
| name = Debbie Does Dallas
| image = Debbiedoesdallas.jpg
| image_size = 225px
| caption = theatrical poster
| director = Jim Clark
| writer = Maria Minestra
| starring = [[Bambi Woods]]&lt;br&gt;Christie Ford&lt;br&gt;[[Robert Kerman]]&lt;br&gt;[[Robin Byrd]]&lt;br&gt;[[Herschel Savage]]&lt;br&gt;[[Eric Edwards (pornographic actor)|Eric Edwards]]&lt;br&gt;Arcadia Lake
| music = Gerald Sampler
| cinematography = Billy Budd
| editing = Hals Liptus
| distributor = VCX, Cabaret Video&lt;ref name=Brooklyn&gt;{{cite book|title=The Brooklyn film: essays in the history of filmmaking|publisher=[[McFarland &amp; Company|McFarland]]|author=John B. Manbeck, Robert Singer |year=2002|url=http://books.google.co.uk/books?id=HH1s4R3d99oC|isbn=0-7864-1405-7|page=193}}&lt;/ref&gt;
| released = 1978&lt;ref name=Brooklyn/&gt;
| runtime = 90 minutes&lt;ref name=Brooklyn/&gt;
| language = English
| budget =
 }}

''''THIS IS A TEST'''' with [[links]] and [[whatever|other links]]. And here is the second line.

{{lolwut}}
"""   


if __name__ == '__main__':
    unittest.main()

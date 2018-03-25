from urllib.request import Request, urlopen, URLError
import requests
import json

NERD_URL = 'http://nerd.eurecom.fr/api/entity?key=9reqenou0oc0dop4aet49kht1eis95d5&idAnnotation=2532326'
YAGO_URL = 'https://api.ambiverse.com/v2/entitylinking/analyze'


yago_headers = {'AUTHORIZATION': '3c3ce1778645ff7740b702ff8cef614d17085ea7', 'Content-Type': 'application/json'}
yago_data = {
  "coherentDocument": True,
  "confidenceThreshold": 0.075,
  "docId": "Test_Tweets",
  "text": "A list of famous people, chosen mainly from the nineteenth, twentieth or twenty-first centuries. This list includes famous actors, politicians, entrepreneurs, writers, artists and humanitarians. Marilyn Monroe (1926 – 1962) American actress, singer, model Abraham Lincoln (1809 – 1865) US President during American civil war Mother Teresa (1910 – 1997) Macedonian Catholic missionary nun John F. Kennedy (1917 – 1963) US President 1961 – 1963 Martin Luther King (1929 – 1968)  American civil rights campaigner Nelson Mandela (1918 – 2013)  South African President anti-apartheid campaigner Queen Elizabeth II (1926 – ) British monarch since 1954 Winston Churchill (1874 – 1965) British Prime Minister during WWII Donald Trump (1946 – ) Businessman, politician Bill Gates (1955 – ) American businessman, founder of Microsoft Muhammad Ali (1942 – 2016) American Boxer and civil rights campaigner Mahatma Gandhi (1869 – 1948) Leader of Indian independence movement Margaret Thatcher (1925 – 2013) British Prime Minister 1979 – 1990 Christopher Columbus (1451 – 1506) Italian explorer Charles Darwin (1809 – 1882) British scientist, theory of evolution Elvis Presley (1935 – 1977) American musician Albert Einstein (1879 – 1955) German scientist, theory of relativity Paul McCartney (1942 – ) British musician, member of Beatles Queen Victoria ( 1819 – 1901) British monarch 1837 – 1901 Pope Francis (1936 – ) First pope from the Americas Jawaharlal Nehru (1889 – 1964) Indian Prime Minister 1947 – 1964 Leonardo da Vinci (1452 – 1519) Italian, painter, scientist, polymath Vincent Van Gogh (1853 – 1890) Dutch artist Franklin D. Roosevelt (1882 – 1945) US President 1932 – 1945 Pope John Paul II (1920 – 2005) Polish Pope Thomas Edison ( 1847 – 1931) American inventor Rosa Parks (1913 – 2005)  American civil rights activist Aung San Suu Kyi (1945 – ) Burmese opposition leader Lyndon Johnson (1908 – 1973) US President 1963 – 1969 Ludwig Beethoven (1770 – 1827) German composer Oprah Winfrey (1954 – ) American TV presenter, actress, entrepreneur Indira Gandhi (1917 – 1984) Prime Minister of India 1966 – 1977 Eva Peron (1919 – 1952) First Lady of Argentina 1946 – 1952 Benazir Bhutto (1953 – 2007) Prime Minister of Pakistan 1993 – 1996 George Orwell (1903 – 1950) British author Desmond Tutu (1931 – ) South African Bishop and opponent of apartheid Dalai Lama (1938 – ) Spiritual and political leader of Tibetans Walt Disney (1901 – 1966) American film producer Neil Armstrong (1930 – 2012) US astronaut Peter Sellers (1925 – 1980) British actor and comedian Barack Obama (1961 – ) US President 2008 – 2016 Malcolm X (1925 – 1965) American Black nationalist leader J.K.Rowling (1965 – ) British author Richard Branson (1950 – ) British entrepreneur Pele (1940 – ) Brazilian footballer, considered greatest of 20th century. Angelina Jolie (1975 – ) Actress, director, humanitarian Jesse Owens (1913 – 1980) US track athlete, 1936 Olympics Ernest Hemingway (1899 – 1961) American author John Lennon (1940 – 1980) British musician, member of the Beatles Henry Ford (1863 – 1947) US Industrialist Haile Selassie (1892 – 1975) Emperor of Ethiopia 1930 – 1974 Joseph Stalin (1879 – 1953) Leader of Soviet Union 1924 – 1953 Lord Baden Powell (1857 – 1941) British Founder of scout movement Michael Jordon (1963 – ) US Basketball star George Bush Jnr (1946 – ) US President 2000-2008 Vladimir Lenin (1870 – 1924) Leader of Russian Revolution 1917 Ingrid Bergman (1915 – 1982) Swedish actress Fidel Castro (1926 – ) President of Cuba 1976 – 2008 Leo Tolstoy (1828 – 1910) Russian author and philosopher Pablo Picasso (1881 – 1973) Spanish modern artist Oscar Wilde (1854 – 1900) Irish author, poet, playwright Coco Chanel (1883 – 1971) French fashion designer Charles de Gaulle (1890 – 1970) French resistance leader and President 1959 – 1969 Amelia Earhart (1897 – 1937) Aviator John M Keynes (1883 – 1946) British economist Louis Pasteur (1822 – 1895) French chemist and microbiologist Mikhail Gorbachev (1931 – ) Leader of Soviet Union 1985 – 1991 Plato (423 BC – 348 BC) Greek philosopher Adolf Hitler (1889 – 1945) leader of Nazi Germany 1933 – 1945 Sting (1951 – ) British musician Mary Magdalene (4 BCE – 40CE) devotee of Jesus Christ Alfred Hitchcock (1899 – 1980) English / American film producer, director Michael Jackson (1958 – 2009) American musician Madonna (1958 – ) American musician, actress, author Mata Hari (1876 – 1917) Dutch exotic dancer, executed as spy Cleopatra (69 – 30 BCE) Queen of Egypt Grace Kelly (1929 – 1982) American actress, Princess of Monaco Steve Jobs (1955 – 2012) co-founder of Apple computers Ronald Reagan (1911 – 2004) US President 1981-1989 Lionel Messi (1987 – ) Argentinian footballer Babe Ruth (1895 – 1948) American baseball player Bob Geldof (1951 – ) Irish musician, charity worker Leon Trotsky (1879 – 1940) Russian Marxist revolutionary Roger Federer (1981 – ) Swiss Tennis player Sigmund Freud (1856 – 1939) Austrian psychoanalyst Woodrow Wilson (1856 – 1924) US president 1913 – 1921 Mao Zedong (1893 – 1976) Leader of Chinese Communist revolution Katherine Hepburn (1907 – 2003) American actress Audrey Hepburn (1929 – 1993) British actress and humanitarian David Beckham (1975 – )  English footballer Tiger Woods (1975 – ) American golfer Usain Bolt (1986 – ) Jamaican athlete and Olympian Carl Lewis (1961 – ) US athlete and Olympian Prince Charles (1948 – )  Heir to British throne Jacqueline Kennedy Onassis (1929 – 1994) American wife of JF Kennedy C.S. Lewis (1898 – 1963) British author Billie Holiday (1915 – 1959) American jazz singer J.R.R. Tolkien (1892 – 1973) British author Billie Jean King (1943 – ) American tennis player and human rights activist Anne Frank (1929 – 1945) Dutch Jewish author who died in Holocaust",
  "language": "en",
  "annotatedMentions": [
    {
      "charLength": 2,
      "charOffset": 0
    }
  ]
}


def callNERD():
	print('calling nerd')
	request = Request(NERD_URL)
	try:
		response = urlopen(request)
		data = response.read()
		print(data)
	except URLError as e:
	    print ('Got an error code:'+ str(e))


def callYAGO():
	print('calling yago')
	try:
		response = requests.post(YAGO_URL, json=yago_data, headers=yago_headers)
		print(response.json())
	except Exception as e:
	    print ('Got an error code:'+ str(e))


# callNERD()
callYAGO()
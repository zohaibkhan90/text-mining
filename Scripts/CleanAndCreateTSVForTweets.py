import re
import ast

output_file = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/super_tuesday/super_tuesday_cleaned_tweets.tsv'
path = '/Users/zohaib/Desktop/Courses/Text-Mining/Data/super_tuesday/super_tuesday_data.txt'
file = open(path,'r')
lineString = file.readlines()
file.close()

TSV_File = open(output_file,'w')
TSV_File.write("Id\tCreated At\tText\n")

###Preprocess tweets
def processTweet2(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet


def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

# text = 'Wasem tek ku bures ki tp jik ktok dingRT @EgaPoch: Alhamdulillah MNC TV kembali cerah, #FACupFinal RT if you would like @lfc to win the FA Cup final today #CFC #LFC #FACupFinal RT @oliverproudlock: Amazing lunch, now settling in for the big game. Come on Chels!! #facup RT @RightToPlay_UK: Not long now till RTP partner @chelseafc take on Liverpool, come on blues! #facup RT if you would like @ChelseaFC to win the FA Cup Final today #CFC #LFC #CFCWembley #FACupFinal RT @danwalkerbbc: Kenny Dalglish has never lost to Chelsea as a manager - 13 games in total! #LFC #CFC #FACupFinal #stat The FACup, as we all know, is dominated by the big clubs almost as xclusively as the Premier League and this year is no different#FAcupFinal RT @juniorbachchan: In keeping with tradition..... Right here right now- fatboy slim. LOUD!!!! #comeonCHELSEA #CFC #KTBFFH RT @ESPNTVUK: Steven Gerrard has just come out onto the pitch. http://t.co/bkmx9IPQ #FACupFinal #lfc #cfc It made us laugh: Watch Jamie Carragher, Steven Gerrard and Pepe Reina play Guess Who - Liverpool FC style http://t.co/7K7vOWQp #LFC let the natty daddys be cracked!!! FA Cup day! cmonnnnnn yoouuuuuu redddssssssssssssssssssssssss #8 #7 #LFC RT @ESPNTVUK: Steven Gerrard has just come out onto the pitch. http://t.co/bkmx9IPQ #FACupFinal #lfc #cfc Here comes that sick feeling in my stomach again! Felt it a lot lately! Come on Chelsea!! #CFC #FACup On days like this, we remember the 96 loved ones who went to watch #LFC get to an FA Cup final but never made it back home. #justice @joefooty @mayurbhanji @TwitPic let their be rain or any other obstacle BUT no one can stop @lfc from taking away the cup from blues Looking forward to watching #facupfinal later just a pity I''ll be watching it at mother in law :-( RT @chelseafc: In the #CFCWembley dressing room right now are the kit boys! #FACupFinal (SL) http://t.co/E0Q9FFET Kenny Dalglish''s eye lids to sag even more today. #FACup #FACT Luis Suarez - best all round Footballer is the Premier League! #fact #LFC All the best to LIVERPOOL all the way from SOUTH AFRICA @LFC, let''s make history here ... @tessalonso that looks amazing!!! I can''t believe you are there!!! Wembley!!!! Come on you Reds!!! #LFC Processing file number57 Retrieved Tweets from file 5_5_2012_14_6.txt RT @snurrashiqah: #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CFC #CF ... Vou terminar de me arrumar e ir encontrar as lindas @_mariifonseca e @kasouza__ para irmos ver o jogo juntas #FACupFinal Getting nervous now, Liverpool need to do the business today to make this season worthwhile! #ynwa #lfc RT @saidraish: RT @ChelseaFansCol: Chelsea solo ha perdido 1 de sus ultimos 33 partidos de FA Cup (excluyendo derrotas en penales). #CFC ... #CHELSEA #CHELSEA #CHELSEA #CHELSEA #CHELSEA !!! #facup #uefa weee goin in haaard!! #LFC #YNWA juara #FACupFinal #LFC #KingKenny RT @ElLoxa: @juankamilomarin ESO. Goticas de valeriana check, 10 bultos llenos de insultos hacia #Reina #Carrol #JoseEnrique check. Vamo ... RT @chelseafc: RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/ZxVOVTOH Just watched The Big Lebowski, very funny. Going for a run now... Triathlon training &amp; then it''s FA cup time #LFC Fingers crossed! Toes crossed! Hands and feet crossed! COME ON U REDS !!! BRING IT HOME !!! #lfc #FACUP ⚽ Big Day Today C''mon Liverpool⚽ #FACupFinal #LFC @Torrrres_ #CFC and that too winning CL... haha good joke mate! Will be routing for #CFC tbh, one I want RDM to get the managers position full time (well deserved and two, they have better looking staff. RT @hidro20: done RT @liverpool: Are you ready for the final? Share your pics... #lfc http://t.co/r8YoZ0Dn Watching from a viewing centre in otuocha nigeria #CFCwembley @chelseafc http://t.co/Wy7auHGB Just watched replays from the Emirates..what a game !.This is what the end of the season is all about!...Hope #CFC come on top today.. let''s go let''s go let''s go!!! #FACupFinal #Chelsea #Liverpool #BluesAllDay #CFCWembley #FACupFinal Chelsea you got this! Kör igång uppladdningen med en Carlsberg. Avspark om knappa 2 timmar. #FaCup #Lfc the #FAcupfinal should be kicking off now 3pm not 5.15pm #whathappenedtotradition @chelsea4girls @chelseafc Ok @stephenfry big shout for team of the season from me! And a I''m a red man #LFC #NCFC RT @Rosscopekotrain: Chelsea, Newcastle United, Manchester United, that will be a superb bank holiday weekend. #FACupFinal #premiership RT @BhavKhoda: Chelsea or Liverpool.. Hmm for me its the reds all the way! #FaCup RT @RokkenStudhus: FA Cup finale 2012: @ChelseaFC vs @LFC på Rokken i dag! Sendingen starter 17:15, kampen 18:15! Bli med, dette blir go ... Blue is the colour! #CFC RT @liverpool Are you ready for the final? Share your pics... #lfc @mshini12 #Emirates #FACUPFINAL #TeamLiverpool Two words for u Siya, #Fernando Tooooooooooooooooooooores!!! Today we will be champions for the honor of our colors! // #ChelseaFC #CFC #CFCWembley #Chelsea #TheBlues ! #FAcup ! @DDotPlayDirty what''s ur predictions for the #FACUP Kalah teu nyaho siah RT @fitrisofy: \(´▽`)/ ‎​\(´▽`)/ RT @liverpool: Are you ready for the final? Share your pics... #lfc Hoy es La final  de la FA Cup, @ChelseaFC Vs Livepool, #GoBlues @LFCTS I say 1 nil #LFC it will be cagey game.. RT @gracedoolan: #LFC #YNWA &lt;3 Yeahhhh!!!! RT @BIGREDS_IOLSC: About 2 hours to go. Are you ready, lads &amp; lasses?! #FACupFinal #LFC #BIGREDS CHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEACHELSEA #CFC Starting to get nervous about the final. #LFC #FACUP RT @LFC: Liverpool fans in fine voice in the pubs around Wembley. Here''s the scene outside the Torch http://t.co/oNlaFxwf Absolutely gutted I''m not at wembley again today but for anyone going have an amazing time! #celery #KTBFFH #CFC shitting it. COME ON RED MEN!  #lfc #facupfinal s/o 2 all chelsea fans!!!!!! Our first trophy 4 d season in sum few hours... #cfc RT @chelseafc: Seems to be drying out in NW London. Fingers crossed! #CFCWembley #FACupFinal (SL) #YNWA RT @liverpool: Are you ready for the final? Share your pics... #lfc @KholzztheFelo I feel so sad for you. @chelseafc @Kaizer_Chiefs @Barcelona Been a bittersweet season, but I''m super excited for this match, for @LFC &amp; for fellow fans the world over! Come on you reds!! #FACup #LFC buzzin for the game, #CFC Chelsea''s FA Cup final shirt. #CFC @Chelseafc http://t.co/ELVGU0ye RT @chelseafc: RT @ryanbertrand3: Come on chelsea! Big day for everyone thats blue! Final days are so good man ... http://t.co/sEO70jKI RT @bluechampion: Remember folks! It''s raining at Wembley! The boy from Spain loves the rain! Fernando to score today! #cfc @chelseafc RT @anditi3: En route Wembley. Come on you blues #cfc @simonrim @simonrim Happy Bday! 3rd win today for the reds against #CFC this season. RT our photo at the semi, #YNWA - http://t.co/GMkpH47i Tks-I hope so, or I''ll be tossing bottles too! #CFC #FACupFinal RT @TheRealTylerH hope your team has a better result then mine did today. RT @umbro: To win signed Andy Carroll Speciali boots, just RT this message before the end of today''s #FACup http://t.co/Mn4uSsn0 @JohnBishop100 walk with us mere mortals! #LFC You never walk alone....hope win tonight @LFC We in this mann!!!RT @mbu2manylaughs: Duuude! RT @MonksDj: Hope its gona b hot game!!!! #FaCupFinal cc @iamjabulation @mbu2manylaughs Yessss #LFC http://t.co/GDTWYYZ4 @ajamazhar95 liverpool ! #YNWA #LFC #thefacup #FACupFinal !  C''Mon #Chelsea ESPN''s build up to the #FACupFinal has been fantastic so far. RT @stuartfergus: 96 angels look on from heaven whilst 11 men fight for their honour and pride! Cmon u red men! #BeScouseBeProud #jft96 #lfc RT @BenSmithBBC: If #LFC win the FA Cup today it would be Dalglish''s 28th major honour at the club. #CFC have won 22 trophies in their h ... RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/8UWDQEM6 would love to be there today, unfortunately #studentism beats me to it but I''ll be representing the Reds in Brum #untillater #lfc #ynwa Hoy un grandísimo partido #GoBlues #CFC #FACup Dalglish: FA Cup win could repay only part of my Liverpool debt | The Guardian http://t.co/t1BSu5zl #LFC Waiting for the #FACupFinal coverage to start on #itvhd and they just broadcast the news and weather from the NW, really handy info in NE RT @thisisanfield: RT if the pre-match nerves are kicking in! #LFC #FACupFinal اصدقائي الليفربولين ابارك لكم الفوز في كأس انجلترا من الان الف الف مبروك 🏆  #ليفربول #YNWA #lfc #LFCAR #facup Best Frivolity Ever http://t.co/5ZqIJNgF @Fran_Riddle sorry cant remember talking about #mufc :| pretty sure I tweeted about #LFC and how biased Hansen and Lawrenson are Can''t hardly wait for the match! #Chelsea #FACupFinal :D chelseafc: RT @AndrewCollins80: Leaving for Wembley, nervous, but pretty sure we can do it!! #comeonyoublues #CFCWembley #KTBFFH #Wembley... Hour left in work then C-Town! #shapnels #facup £10 bet on the #facupfinal, come onnnn Liverpool! @lukemayyy wanna come to mine and watch the #facupfinal ?! #lfc http://t.co/SVPXaj1p Good luck to @LFC in the FA Cup final today! Here''s our own (fitting) red banner!  @CampandFurnace 22.5.12 #LFC http://t.co/uzuz5mcM Probally line-up: Cech, Bosingwa, Ivanovic, Terry, Cole, Meireles, Ramires, Mata, Lampard, Drogba, Torres. This is my prediction. @chelseafc RT @liverpool: Are you ready for the final? Share your pics... #lfc RT @OfficialSF1Team: Wishing all the best to @chelseafc in the   #FACupFinal @Wembley! Let''s get the trophy! Mau @chelseafc  atau @LFC yg menang, bakal tetep seneng :D Ha ha #l''arse could have put #cfc out of the equation for 3rd 2 decent wins means we can do it need spurs and nufc poor wins RT: @AndrewCollins80: Leaving for Wembley, nervous, but pretty sure we can do it!! #comeonyoublues #CFCWembley #KTBFFH #WembleyKings Keep the blue flag high! #CFC #KTBFH RT @timlovejoy: So met up with @simonrim at Wembley #facup http://t.co/cSb0UqPm @adhisofyan skormu loh ngayal hahaha @LiverpoolFC yang juara, #chelsea puasa gelar musim ini @MannanJamil17 @chelseafc yeaah defo chelseafc: RT @bluechampion: Remember folks! It''s raining at Wembley! The boy from Spain loves the rain! Fernando to score today! #cfc @c... 2 hours til kick off. #ynwa #facupfinal #lfc #gerrard http://t.co/k9pTgPOM ลิเวอร์พูลนายแพ้แน่ ! (มั้ง) 555 #FACupFinal About to get on the tube, buzzing my nads off for the game, beer is needed! #CFC RT @ESPNTVUK: The FA Cup is in pride of place, pitchside at Wembley. Who will lift it this evening? #CFC or #LFC? #FACupFinal http://t.c ... @AsianprincessXo @chrismufc4life getting jls:D #cfc #mcfc RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/8UWDQEM6 #LFC win the battle of the fans hands down! Chelscum couldn''t even sell their allocation! #worstfansintheworld  http://t.co/ap84rn3w #ComeOnLiverpool #LFC #FACupFinal From Mexico, ready for the final! @chelseafc #CFCWembley RT @chelseafc: Send us your pics of the day using #CFCWembley and we''ll RT our faves as always. #FACupFinal (SL) chelseafc: Send us your pics of the day using #CFCWembley and we''ll RT our faves as always. #FACupFinal (SL) I need to have a wise man telling me that #LFC will win today! I''m sooooo nervous! GET IN THERE YOU #REDS Goodluck @chelseafc in the FA Cup final! Fancy El Nino to win it ☺ RT @kukuhprstyo: i love you @chelseafc , come on, no one can stop us !! Pride of london Just a couple of hours to go. Come on @LFC #YNWA #FACup RT @thisisanfield: Rationale for that team; Kuyt to work hard to stop Cole''s threat from left back; Bellamy to capitalise on Bosingwa on ... chelseafc: RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/wXszaQof RT @Jay_78_: #LFC Drogba banner again http://t.co/SoUP9VAN Chelsea le ha anotado 226 goles al Liverpool, y ha recibido 246. #CFCWembley hoping for the best @chelseafc @Chelseafc vs @LFC The hype for big matches end up being shit matches #FACupFinal RT @adidasUK: NEWSFLASH: We''ve got a signed @chelseafc shirt up for grabs ahead of today''s all-adidas #FaCUPfinal showdown... http://t.c ... #lfc @DikacyTheGreat win they didn''t too lol. on a blue note #FACupFinal #CFC RT @Jay_78_: "She loves the scouse cock, she loves the scouse cock...John Terry''s ma...she loves the scouse cock" #LFC #CFC Off to watch #facupfinal at mumma''s house in a bit then got tickets booked to see #Avengers3D after! Just what the doctor ordered :) Now: LFC TV live from Wembley - Liverpool FC http://t.co/thapBw0W via @lfc @manimal666 haha at work mate, sodding off soon for footy though :) #LFC How''s tricks with you? @LFC win win win! #YNWA RT @GIGIpetite1: RT this to wish the boys luck for today''s final! #LFC #ynwa #zootwitties #bumblr #gigibum @ZOO_UK @LFC @lfcgossip http: ... #ComeOnYouBlueBoys @chelseafc We need to be back here winning this.... #lfc #ynwa http://t.co/gjTLxYSA Power e/w and Top Offer win #Guineas. Fancy #cfc to win the FA Cup Final aet. O''Sullivan to WSC. What a weekend of sport this is! RT: "@talkSPORT: Former Liverpool captain says league position is more important than cup wins: http://t.co/aU2diXnX #LFC" Processing file number58 Retrieved Tweets from file 5_5_2012_14_7.txt RT @CFCchants: Torres! Torres! He left The Kop to join The Shed.. Torres! Torres! He forced Liverfool to panic buy,Now they chanting Car ... hahaha keep getting liverpool fan groups and stuff follow me woo! #lfc You''ll never walk alone! #YNWA #LFC RT @alrickbrown: Since 2006 Frank Lampard has scored more goals than any other player in the FA Cup (19). #Chelsea #FACupFinal #CFC RT @redisticwear: About 2 hours to go #FACUPFINAL #LFC #WEMBLEY #FACUP K.O Is At 5 -_- @johncrossmirror I agree with you. Wenger is paying the price for being too over cautious. RT @ChelseaUnite: TONIGHT!!! FINAL #FAcup Chelsea v Liverpool KO 23:15 WIB! LIVE at MNCtv/ESPN! We''re gonna make this a BLUE DAY! #CU RT @henrywinter: Front of £10 #cfc v #lfc FA Cup final programme... Drogba v Skrtel http://t.co/IPmVr5i9 Bismillah malam untuk @chelseafc semoga amin ! ''Come on You Blues!!! ... #THEMAGICOFTHECUP ... http://t.co/94rQYvEe via @wordpressdotcom #CFC #ChelseaFC #teamchelsea http://t.co/a2V5MShs RT @BaseAllstar: For cup final day I present my 2 year old son singing Luis Suarez: http://t.co/BebVGQ4B via @youtube #LFC #YNWA Right, there''s a long build up to the football match. I''ll probably getting stupidly excited by aerial shots of my manor #FACupFinal Amidaus top its zone(3A) with 26pts after 12games.scored 19 nd conceeded 4.#facup#ghfooty @Zaahid_lfc kits out his room for the big occasion. #YNWA #FACupFinal http://t.co/OZl672pU RT @Jay_78_: "She loves the scouse cock, she loves the scouse cock...John Terry''s ma...she loves the scouse cock" #LFC #CFC Would rather go to @lfctv than the itv build up! #lfc RT @liverpool: RT @hidro20: done RT @liverpool: Are you ready for the final? Share your pics... #lfc http://t.co/r8YoZ0Dn But first, i''m heading to the virgin river casino here in mesquite to try and watch the fa cup final #ktbffh #cfc Chelsea (¬_¬") RT @adiELLAdiELLA: @LFC (Liverpool) ! !!!! RT @dhilayou: Bakal dukung chelsea nih (ง''̀⌣''́)ง RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/8UWDQEM6 #LFC #YNWA cant wait for kick off #FACup starts in 2 hours, so get your bets on now and earn up to $200 in free betting money! http://t.co/wamALkdP  #EPL #Chelsea #Liverpool @chelseafc wishing you all a good luck at wembley. My predictions chelsea 2-1 liverpool RT @adidasUK: To win a signed shirt, get involved &amp; #takethestage: @chelseafc fans (http://t.co/HtfDWvg9) vs. @LFC fans (http://t.co ... Excited to see @LFC take home the FA Cup. #BeatChelsea RT @Naziho_Torres9: Let''s do it tonight! #CFC Ahh... Why does work have to be soo boring? 😒 Looking forward to the #FACupFinal later tho! Hoy seremos campeones por el honor de nuestros colores! // #ChelseaFC #CFC #CFCWembley #Chelsea #TheBlues ! #FAcup @chelseafc what time chelsea vs liverpool ? Best banner today! #cfc #lfc #ktbffh #ynwa  http://t.co/F4goZPQI I have had my #cfc shirt on since half 7 this mornin I''m going out tonight if we win I will wear it all night.........come on @chelseafc I am waiting on you Chelsea @chelseafc #CFC Vs #Liverpool RT @AimanMahzan: RT @SureiyanHamond: Can''t wait for the FA Cup final. Bak datang la Chelsea! #LFC boleh! ☺ RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/8UWDQEM6 Come on you blues   #FAcupfinal. RT @liverpool: RT @hidro20: done RT @liverpool: Are you ready for the final? Share your pics... #lfc http://t.co/r8YoZ0Dn Enjoying the build up. Just like the old days actually making me keen to watch the game#FACupfinal RT @bluechampion: Remember folks! It''s raining at Wembley! The boy from Spain loves the rain! Fernando to score today! #cfc @chelseafc good luck to the boys in red @LFC for today''s FA Cup final! x #youllneverwalkalone Dalglish alone has 27 trophies with #LFC. #CFC have won 22 trophies throughout their entire history. RT @Jay_78_: #LFC Drogba banner again http://t.co/SoUP9VAN RT @LiverpooIFCNews: RT @Jay_78_: #LFC Drogba banner again http://t.co/3LdQXAbW RT @Jay_78_: "She loves the scouse cock, she loves the scouse cock...John Terry''s ma...she loves the scouse cock" #LFC #CFC Just over 2 Hours to kick off for the #FACUP. Gotta get these wedding photos finished before than. C''mon the Reds #LFC @bluechampion @chelseafc @chelseafc up blue...!!!elnino has to score.. As the time draws closer....nail-biting moments #FACup #wembleyIsBlue #CFC @damostriker Agree! 5.15 is a joke. Turning Cup Final Day into Cup Final Evening has killed the magic. #FACup RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/8UWDQEM6 Just done Chelsea to win 2-1 and Torres to score first. Come on lads! #CFCWembley #FACupFinal RT @InformeFutVen: Comunicado Del #CFC: Se participa a la barra del equipo visitante, tras sanción impuesta por parte de la FVF, no podr ... Are the Americans ready yet for the #FACupFinal .i hope so.... All this waiting is for them #Budweisercup RT @Jay_78_: #LFC Drogba banner again http://t.co/SoUP9VAN RT @bluechampion: Remember folks! It''s raining at Wembley! The boy from Spain loves the rain! Fernando to score today! #cfc @chelseafc Didier Drogba has scored In all of his seven appearances at Wembley. I expect him to carry that on today. #Cfc #FAcupFinal RT @bluechampion: Remember folks! It''s raining at Wembley! The boy from Spain loves the rain! Fernando to score today! #cfc @chelseafc RT @AndrewCollins80: Leaving for Wembley, nervous, but pretty sure we can do it!! #comeonyoublues #CFCWembley #KTBFFH #WembleyKings Feeling lucky for #Chelsea''s game today #comeonyoublues #CFC #KTBFFH @JamieDalton82 Arsenal can afford to lose RVP but can''t Koscielny RT @Jay_78_: #LFC Drogba banner again http://t.co/SoUP9VAN #REDARMY #YNWA #LFC COME ON YOU REDS! I 💙 Chelsea FC. Let''s paint Wembley blue and get our first trophy of the season! #KTBFFH #CFCWembley @mnhabs Go Reds! #FACup Arsenal''s game over. I''m out for supper. #FAcup final not interested. RT @ZIYAAD_LFC: From Maradona, with love! #YNWA #LFC http://t.co/mih6B5d0 #facupfinal All Set! COME ON #CFC RT @MauraONeill1: @damostriker Agree! 5.15 is a joke. Turning Cup Final Day into Cup Final Evening has killed the magic. #FACup I don''t know who I want to win but I just want a sick game! #FACupFinal @chelseafc RT @IDmensbiore: Siap-siap nonton Final FA Cup 2012 ??!! LIVERPOOL vs CHELSEA kira-kira siapa yang jadi Juara FA 2012 Bro? "@LFCNY: 5 European cups, 18 leagues, that''s what we call history....you know the rest." LETS GO LIVERPOOL! #FACup Reds, Blues ? On vote blanc ! http://t.co/i9rNxK7p #facup #liverpool #chelsea #wembley @chelseafc come on you blues, we can do this!! Blue is the colour!! I want to see Torres grab a goal #COYB #chelseano9 #KTBFFH #FACup Buzzing for todays game :) :) Good Luck Lads @lfc  YNWA @MannanJamil17 @chelseafc nope going tomoz why ? Today defense was all over the place. From 1to 90 mins back 4 were out of sorts. Was #cfc prayings in Wembley influenced the game? Lolz Sorry but what''s with the #facupfinal kicking off at 5.15?  It should always be a 3pm ko.  No argument. RT @CFCchants: Torres! Torres! He left The Kop to join The Shed.. Torres! Torres! He forced Liverfool to panic buy,Now they chanting Car ... from Stamford Bridge to Wembley, we''ll Keep The Blue Flag Flying High #CFC #KTBFFH @Naazraj boss , tonight ? 12:45 #LFC #CFC #CFCWembley #COYB ⚽⚽⚽⚽⚽ RT @thefadotcom: The FA will donate £1 for every #FACup Final match programme sold to the charity Cardiac Risk in the Young (@CRY_UK)htt ... RT @2Ferdi7: There''s still four hours to go and I''m already drunk, kitted out in my scarf and a bag of nerves #LFC #FACupFinal #LFCFamily RT @redisticwear: About 2 hours to go #FACUPFINAL #LFC #WEMBLEY @johncrossmirror maybe, he''s better as an impact player for now with a team on the ropes playing against tired defenders? RT @stamfordsally15: I 💙 Chelsea FC. Let''s paint Wembley blue and get our first trophy of the season! #KTBFFH #CFCWembley FA CUP, CHAMPIONS LEAGUE #cfc RT @BIGREDS_IOLSC: About 2 hours to go. Are you ready, lads &amp; lasses?! #FACupFinal #LFC #BIGREDS #Cfc #Cfc #Cfc #Cfc #Cfc #Classic RT @lfcgossip: RT @Bethany_LFC: #LFC banners going to Wembley. Some crackers in there! (frm:rawk). #facup http://t.co/0zY3cNEj At wembley stadium more reds than blues! Atmosphere is amazing #FACUP Good banner. ''S''appenin'' Wembley'' #lfc@wembley @chelseafc ...we run Wembley #GoBlues @JayGShore Liverpool to win 2-1 come on you reds #LFC x FA CUP Winner is LIVERPOOL @LFC !!!!  #YNWA #JFT96 Today #Wembley will be #Red ! #LIVERPOOL #YNWA :D @TristanP84 Torres and Carroll combine to score 7 goals...only because everyone else gets red carded out of the game. #LFC wins 4-3. It''s Cup Final day - come on you Reds! #LFC #FACupFinal Reina: Torres Would Have Regretted Leaving Liverpool: Pepe Reina believes that Fernando Torres would have r... http://t.co/RTjFhItA #LFC I really hope El Nino scores today against Loserpool ! KTBFFH #CFC #CHELSEA #FACUP #goblues VAMOOOS CHELSEAAAAAA @johncrossmirror Ox needs to weaken AW''s grandson in Ramsey before he can get games. @chelseafc I wish you all the world''s Lucky to beat the LCF #CFCWembley @johncrossmirror why wenger doesnot change his formation and what we need to do to get ramsey dropped. Awful player Trying my best to stay awake for the #FACUP so excited for the game today! #FACup #LFC RT @LewisWiltshire: For the Cup Final in England, use the hashtag #FACupFinal to join the conversation with @LFC @chelseafc @thefadotcom ... gk sabar lounching jersey @LFC 2012/2013 RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/8UWDQEM6 todays game will be tight, 2-1 liverpool. i reckon! COME ON YOU REDS! ❤ #LFC #ynwa #Liverpool fans, 3/1 on you to win the FA Cup. Sign up here http://t.co/sBrTeuNM then bet here http://t.co/LBTWo32F #LFC @Jones2406 @chelseafc you at dads ? RT @chelsea4girls: @chelseafc #CFCWembley cup of Chelsea tea before kick off! http://t.co/8UWDQEM6 RT @jemmy_23: 22.30 please come faster #FACupFinal" At the end of the storm, theres a golden sky… @LFC #YNWA Congratulations to Chelsea fans, you''ve managed to sink even lower with the cynical use of the ''39'' stickers - didn''t think it possible #lfc Why couldn''t the fa leave the final on at a decent time I''d be watchin soccer now instead of mouk #LFC #FACup2012 #InKennyWeTrust #Disney RT @C_Bester: Nearly an hour until kick off!! @nickbester18 @LFC @Crawshay_Hall @dylansharp10 RT @TamarTotty: Really classy Chelsea, really classy. #FACUPFINAL #LFC #CFC http://t.co/7FBZ4y5a RT @liverpool: Are you ready for the final? Share your pics... #lfc Genuinely scared for the match #lfc #ynwa Processing file number59 Retrieved Tweets from file 5_5_2012_14_8.txt My celebratory sticky toffee pudding for the cup final today... Or a pick me up if we loose #LFC http://t.co/On89FIwd RT @lampsindofans: Can''t hardly wait for the match! #Chelsea #FACupFinal :D RT @lampsindofans: Can''t hardly wait for the match! #Chelsea #FACupFinal :D It does not feel like 6 years ago that Liverpool beat West Ham in the FA cup final. It was match that got me hooked on football :) #LFC Got the PMT #LFC #YNWA #FACupFinal RT @lampsindofans: Can''t hardly wait for the match! #Chelsea #FACupFinal :D @HarryPaye woooohoooooooooooo #facup i got beer and crisp. I should if popped round yours. How rude me “@mstrdrmz: Best #lfc banner I''ve seen #facupfinal #skrtel #ynwa http://t.co/ICafWiYz” quality Come on king kenny bring the cup up north #FACup final #LFC Today we bring home the FA Cup and fill the trophy case with the most silver ever! #LFC @chelseafc believing in the blues today we can do it we will sing john terrys won the double again this season, rdm full time manager! #cfc House work done. Near pub time!  come on @LFC @turk_79 u coming down for the game? RT @bluechampion: Remember folks! It''s raining at Wembley! The boy from Spain loves the rain! Fernando to score today! #cfc @chelseafc Gone for the shirt we beat united 4 1 in! #retro come on boys!!! #LFC #YNWA @thisisanfield @LFC http://t.co/ja4zFNYY So #AFC fans will be #MCFC fans tomorrow? Along with #LFC #THFC #CFC fans.... 2hr to #FACupFinal kickoff! Me &amp; Dad celebrating a win #LFC :-) http://t.co/d1OMV0m1 RT @Jay_78_: #LFC Drogba banner again http://t.co/SoUP9VAN off to get some food then i go catch the game over a brew. #LFC #cmonyoumightyreds RT @Jay_78_: #LFC Drogba banner again http://t.co/SoUP9VAN I am so nervous now, can''t sit still, please let it be our day #FACup #LFC c''mon Liverpool! logo mais jogo do @chelseafc go blues Hush..halig,nyingkah siah ! RT @16RACHMAT: Forza Chelsea !! RT @ZeniMaarij: You''ll Never Walk Alone !! #Final_FACup #Wembley RT @liverpool_kr: 리버풀 최종훈련영상 RT @MostarLFC: FA Final Last Training Video by shopgirl157 #LFC http://t.co/hjGVyMIu Watching the countdown to the Cup Final on @LFCTV #YNWA #LFC #COYR #FACUP RT @jdufault12: Huge one today at #wembley.  Come on @chelseafc!!  #CFCWembley #supertorres @LucieDingle Does this mean we are going to be rivals for the first time today D?? #LFC  What the hell #powerrangers ?? RT @liverpool: RT @hidro20: done RT @liverpool: Are you ready for the final? Share your pics... #lfc http://t.co/r8YoZ0Dn RT @superstarflash: Chelsea let''s get that first trophy ! #FACUP #Chelseablues ! #facupfinal This is a right place if you are looking for precise type of fantastic piece of information  http://t.co/eyFsotpY And so now destiny calls us, all roads lead to London again, we''ll tread the path of legends inspired by an eternal flame #FACupFinal @CrazyDaveKopite good luck today Make a noise for the red boys #lfc RT @leesiemaszko: RT this pic plse reds fans, #FACupFinal #ChelseaScum #Disrespect #JFT96 #LFC #YNWA http://t.co/xQFWh8Kk @DanEasterby I know right!!! Quite looking forward to it #facup #lfc #MCFC (•̀_•́)ง RT @hilyaiong: #LFC (•̀_•́)ง RT @DStv: Who will leave the Wembley Stadium #FACup Champions? Chelsea vs Liverpool on SS3 from 17:00 http://t.co/MHxXZ5MV Off we go. #Facupfinal http://t.co/b5sZb5Mz So who''s going to win the FA Cup today? Let us know! http://t.co/gJTFPD7P #FACup #LFC #CFC #FIFA12 RT @mrjakehumphrey: Shhhh...surely no-one will notice if I ''borrow'' it for my mantelpiece, will they..? #FACupFinal http://t.co/8LWkwFez RT @Bondie11: Didier Drogba has scored In all of his seven appearances at Wembley. I expect him to carry that on today. #Cfc #FAcupFinal RT @bluechampion: Remember folks! It''s raining at Wembley! The boy from Spain loves the rain! Fernando to score today! #cfc @chelseafc #onedimatteo!&lt;3 he has came and saved us let''s make it our fifth cup in 7 years! @chelseafc RT @liverpool_kr: 런던에 도착한 리버풀 선수들 영상 RT @MostarLFC: The Reds arrive in London video by shopgirl157 #LFC http://t.co/Fagnu4Yh RT @chelseafc: Send us your pics of the day using #CFCWembley and we''ll RT our faves as always. #FACupFinal (SL) Leaving for Wembley. XD. Chelsea all the way #CFCWembley On my way to #Wembley with @chrisbalafas for the FA Cup. 48 hours in london. #Facupfever #CFCWembley #KTBFFH good luck... (2 hour) back to New Wembley stadium ''''@LiverpoolFC'''' #wem8ley #YNWA #FACUPFINAL :* RT @iqball_hXc: #LFC #YNWA juara @chelseafc some support from the states..... LET''S DO THISSSS http://t.co/8Kwhun3C Don''t understand why it kicks off at 5:15. Much better at 3 o''clock!#Facupfinal RT @talkSPORT: Former Liverpool captain says league position is more important than cup wins: http://t.co/76kvRK0l #LFC @chelseafc we sure solely behind you today!!! RT @TruebluesIndo: TONIGHTT!!! FA Cup Final Wembley, Chelsea vs Liverpool. Sabtu, 5 Mei Kick-Off 23.15 WIB live at @BPL_MNCTV ! Don''t mi ... faktor keberuntunganRT @ChelseaNewsID: Chelsea memenangkan semua (6) pertandingan Piala FA yang dimainkan di New Wembley Stadium. #CFC'



count = 0;

for value in lineString:
    val2 = ast.literal_eval(value)
    # print ("id str: "+val2['id_str'])
    # print ("id str: "+val2['created_at'])
    # print ("origional text: "+val2['text'])
    # print ("processed text: "+processTweet2(val2['text']))    
    count = count+ 1
    if count%10000==0:
        print ("Cleaned Tweets: "+ str(count))
    if val2['lang'] == 'en':
        TSV_File.write(val2['id_str']+"\t"+val2['created_at']+"\t"+processTweet2(val2['text'])+"\n")
    

TSV_File.close()


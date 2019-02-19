from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import System, Base, GameItem, User

engine = create_engine('sqlite:///systemgamewithusers.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

User1 = User(name="Mister User", email="taylor.kalajian@mah.org")
session.add(User1)
session.commit()
# GameItem for ps4
system1 = System(user_id=1, name="PlayStation 4")

session.add(system1)
session.commit()

gameItem2 = GameItem(user_id=1, name="Bloodborne", description="Bloodborne is an action role-playing game developed by FromSoftware and published by Sony Computer Entertainment for PlayStation 4. Announced at Sony's E3 2014 conference, the game was released worldwide in March 2015.",
                     genre="Action/RPG", system=system1)

session.add(gameItem2)
session.commit()


gameItem1 = GameItem(user_id=1, name="Destiny", description="Destiny is an online-only multiplayer first-person shooter video game developed by Bungie and published by Activision. It was released worldwide on September 9, 2014, for the PlayStation 3, PlayStation 4, Xbox 360, and Xbox One consoles.",
                     genre="Shooter/RPG", system=system1)

session.add(gameItem1)
session.commit()

gameItem2 = GameItem(user_id=1, name="Red Dead Redemption 2", description="Red Dead Redemption 2 is a Western action-adventure game developed and published by Rockstar GameItem. It was released on October 26, 2018, for the PlayStation 4 and Xbox One consoles. The third entry in the Red Dead series, it is a prequel to the 2010 game Red Dead Redemption.",
                     genre="Action/RPG", system=system1)

session.add(gameItem2)
session.commit()




# GameItem for PS3
system2 = System(user_id=1, name="PlayStation 3")

session.add(system2)
session.commit()


gameItem1 = GameItem(user_id=1, name="Red Dead Redemption", description="Red Dead Redemption is a Western-themed action-adventure game developed by Rockstar San Diego and published by Rockstar GameItem. A spiritual successor to 2004's Red Dead Revolver, it is the second game in the Red Dead series, and was released for the PlayStation 3 and Xbox 360 in May 2010.",
                     genre="Action/RPG", system=system2)

session.add(gameItem1)
session.commit()

gameItem2 = GameItem(user_id=1, name="Demon Souls", description="Demon's Souls is an action role-playing game developed by FromSoftware for the PlayStation 3. It was published in Japan by Sony Computer Entertainment in February 2009, in North America by Atlus USA in October 2009, and in Australia and Europe by Namco Bandai GameItem in June 2010.", genre="Action/RPG", system=system2)

session.add(gameItem2)
session.commit()

gameItem3 = GameItem(user_id=1, name="Little Big Planet", description="LittleBigPlanet is a puzzle platform video game series created by Media Molecule and published by Sony Computer Entertainment on multiple PlayStation platforms. The series follows the adventures of Sackboy and has a large emphasis on gameplay rather than being story-driven.",
                     genre="Puzzle/Platformer", system=system2)

session.add(gameItem3)
session.commit()

gameItem4 = GameItem(user_id=1, name="Bioshock 2", description="BioShock 2 is a first-person shooter video game developed by 2K Marin and published by 2K GameItem. A part of the Bioshock series, it is the sequel to the 2007 video game BioShock and was released worldwide for Microsoft Windows, the PlayStation 3, and the Xbox 360 on February 9, 2010.",
                     genre="Shooter", system=system2)

session.add(gameItem4)
session.commit()



# GameItem for PS2
system1 = System(user_id=1, name="PlayStation 2")

session.add(system1)
session.commit()


gameItem1 = GameItem(user_id=1, name="Fatal Frame 2", description="Fatal Frame II: Crimson Butterfly, known in Europe as Project Zero II: Crimson Butterfly, is a Japanese survival horror video game developed and published by Tecmo in 2003 for the PlayStation 2.",
                     genre="Survival Horror", system=system1)

session.add(gameItem1)
session.commit()

gameItem2 = GameItem(user_id=1, name="Silent Hill 2", description="Silent Hill 2 is a survival horror video game published by Konami for the PlayStation 2 and developed by Team Silent, part of Konami Computer Entertainment Tokyo. It was released in September 2001 as the second installment in the Silent Hill series.",
                     genre="Survival Horror", system=system1)

session.add(gameItem2)
session.commit()

gameItem3 = GameItem(user_id=1, name="Persona 3", description="Persona 3 is a role-playing video game developed by Atlus, and chronologically the fourth installment in the Persona series, a subseries of the Megami Tensei franchise.",
                     genre="RPG", system=system1)

session.add(gameItem3)
session.commit()

gameItem4 = GameItem(user_id=1, name="Persona 4", description="Persona 4 is a role-playing video game developed and published by Atlus for Sony's PlayStation 2, and chronologically the fifth installment in the Persona series, itself a part of the larger Megami Tensei franchise. The game was released in Japan in July 2008, North America in December 2008, and Europe in March 2009.",
                     genre="RPG", system=system1)

session.add(gameItem4)
session.commit()




# GameItem for Switch
system1 = System(user_id=1, name="Nintendo Switch")

session.add(system1)
session.commit()


gameItem1 = GameItem(user_id=1, name="Super Mario Odyssey", description="Super Mario Odyssey is a platform game published by Nintendo for the Nintendo Switch on October 27, 2017.",
                     genre="Platformer", system=system1)

session.add(gameItem1)
session.commit()

gameItem2 = GameItem(user_id=1, name="Super Smash Brothers Ultimate", description="Super Smash Bros. Ultimate is a 2018 crossover fighting game developed by Bandai Namco Studios and Sora Ltd. and published by Nintendo for the Nintendo Switch. It is the fifth installment in the Super Smash Bros. series, succeeding Super Smash Bros. for Nintendo 3DS and Wii U.",
                     genre="Fighting Game", system=system1)

session.add(gameItem2)
session.commit()

gameItem3 = GameItem(user_id=1, name="Enter the Gungeon", description="Enter the Gungeon is a bullet hell roguelike video game developed by Dodge Roll and published by Devolver Digital. It follows four adventurers as they descend into the Gungeon to find a gun to kill their past.",
                     genre="Rogue-Like", system=system1)

session.add(gameItem3)
session.commit()

gameItem4 = GameItem(user_id=1, name="Pokemon: Let's Go Eevee", description="Pokemon: Let's Go, Pikachu! and Pokemon: Let's Go, Eevee! are role-playing video games developed by Game Freak and published by The Pokemon Company and Nintendo for the Nintendo Switch. The games are the first main series Pokemon entries for the Switch, and the first main titles to be released on a home console.",
                     genre="RPG", system=system1)

session.add(gameItem4)
session.commit()

gameItem5 = GameItem(user_id=1, name="The Legend of Zelda: Breath of the Wild", description="The Legend of Zelda: Breath of the Wild is an action-adventure game developed and published by Nintendo. An entry in the longrunning The Legend of Zelda series, it was released for the Nintendo Switch and Wii U consoles on March 3, 2017.",
                     genre="Adventure", system=system1)

session.add(gameItem5)
session.commit()



# GameItem for N64
system1 = System(user_id=1, name="Nintendo 64")

session.add(system1)
session.commit()


gameItem1 = GameItem(user_id=1, name="The Legend of Zelda: Majora's Mask", description="The Legend of Zelda: Majora's Mask is an action-adventure video game developed and published by Nintendo for the Nintendo 64. It was released in 2000 as the sixth main installment in The Legend of Zelda series and was the second to use 3D graphics, following 1998's The Legend of Zelda: Ocarina of Time.",
                     genre="Adventure", system=system1)

session.add(gameItem1)
session.commit()

gameItem2 = GameItem(user_id=1, name="The Legend of Zelda: Ocarina of Time", description="The Legend of Zelda: Ocarina of Time is an action-adventure game developed and published by Nintendo for the Nintendo 64. It was released in Japan and North America in November 1998, and in Europe and Australia the following month.",
                     genre="Adventure", system=system1)

session.add(gameItem2)
session.commit()

gameItem3 = GameItem(user_id=1, name="Super Smash Bros.", description="Super Smash Bros. is a crossover fighting video game developed by HAL Laboratory and published by Nintendo for the Nintendo 64. It was first released in Japan on January 21, 1999, in North America on April 26, 1999, and in Europe on November 19, 1999.",
                     genre="Fighting Game", system=system1)

session.add(gameItem3)
session.commit()



# GameItem for PC
system1 = System(user_id=1, name="PC")

session.add(system1)
session.commit()


gameItem1 = GameItem(user_id=1, name="Magic The Gathering: Arena", description="Magic: The Gathering Arena is a free-to-play digital collectible card game developed by Wizards of the Coast's internal development studio, Wizards Digital GameItem Studio.",
                     genre="Collectible Card Game", system=system1)

session.add(gameItem1)
session.commit()

gameItem2 = GameItem(user_id=1, name="Overwatch", description="Overwatch is a team-based multiplayer first-person shooter video game developed and published by Blizzard Entertainment, which released on May 24, 2016 for PlayStation 4, Xbox One, and Windows.",
                     genre="Shooter", system=system1)

session.add(gameItem2)
session.commit()

gameItem3 = GameItem(user_id=1, name="Guild Wars 2", description="Guild Wars 2 is a massively multiplayer online role-playing game developed by ArenaNet and published by NCSOFT.",
                     genre="MMORPG", system=system1)

session.add(gameItem3)
session.commit()

gameItem4 = GameItem(user_id=1, name="Path of Exile", description="Path of Exile is a free-to-play action role-playing video game developed and published by Grinding Gear GameItem. Following an open beta phase, the game was released in October 2013. A version for Xbox One was released in August 2017 and a PlayStation 4 version is scheduled for release in February 2019.",
                     genre="Action/RPG", system=system1)

session.add(gameItem4)
session.commit()

gameItem2 = GameItem(user_id=1, name="Warframe", description="Warframe is a free-to-play cooperative third-person shooter video game developed and published by Digital Extremes. Originally released for Microsoft Windows in March 2013, it was later ported to the PlayStation 4, Xbox One, and Nintendo Switch.",
                     genre="Shooter/RPG", system=system1)

session.add(gameItem2)
session.commit()


# GameItem for gamecube
system1 = System(user_id=1, name="Nintendo Gamecube")

session.add(system1)
session.commit()

gameItem9 = GameItem(user_id=1, name="Super Mario Sunshine", description="Super Mario Sunshine is a platform game developed and published by Nintendo for the GameCube. It was first released in Japan on July 19, 2002, and was later released in North America, Europe and Australia. It is the second 3D platformer in the Super Mario series, following Super Mario 64 in 1996.",
                     genre="Platformer", system=system1)

session.add(gameItem9)
session.commit()


gameItem1 = GameItem(user_id=1, name="The Legend of Zelda: The Wind Waker", description="The Legend of Zelda: The Wind Waker is an action-adventure game developed and published by Nintendo for the GameCube home video game console. The tenth installment in The Legend of Zelda series, it was released in Japan in December 2002, in North America in March 2003, and in Europe in May 2003.",
                     genre="Adventure", system=system1)

session.add(gameItem1)
session.commit()

gameItem2 = GameItem(user_id=1, name="Super Smash Bros. Melee", description="Super Smash Bros. Melee is a crossover fighting video game developed by HAL Laboratory and published by Nintendo for the GameCube. It was first released in Japan on November 21, 2001, in North America on December 3, 2001, in Europe on May 24, 2002, and in Australia on May 31, 2002.",
                     genre="Fighting Game", system=system1)

session.add(gameItem2)
session.commit()


print("added game items!")
import random
import time as t
import discord
from discord.ext import commands
from discord import app_commands


class CommandeBiscuitChinois(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="biscuit-chinois", description="Vous donne un message positif et motivant, comme un biscuit de fortune.")
    @app_commands.choices(hidden=[
        app_commands.Choice(name="✅", value="true"),
        app_commands.Choice(name="🚫", value="false")
    ])
    async def biscuit_chinois(self, interaction: discord.Interaction, hidden: str = "false"):
        hidden_bool = hidden == "true"
        phrases_motivantes = [
            "Continuez à avancer, quoi qu'il arrive.",
            "Chaque défi est une opportunité de grandir.",
            "Le succès commence par un premier pas.",
            "Votre seule limite est celle que vous vous imposez.",
            "Le progrès, pas la perfection.",
            "Les gagnants n'abandonnent jamais et ceux qui abandonnent ne gagnent jamais.",
            "Les chemins difficiles mènent souvent à de belles destinations.",
            "Le travail acharné bat le talent quand le talent ne travaille pas dur.",
            "La discipline est le pont entre les objectifs et l'accomplissement.",
            "Repoussez vos limites, car personne ne le fera pour vous.",
            "Rêvez-le. Croyez-le. Réalisez-le.",
            "Les petites actions quotidiennes mènent à de grands résultats.",
            "Vous n'avez pas besoin d'être excellent pour commencer, mais vous devez commencer pour devenir excellent.",
            "L'échec n'est pas l'opposé du succès, il en fait partie.",
            "La seule façon d'échouer, c'est d'abandonner.",
            "Prenez des risques. Si vous gagnez, vous serez heureux. Si vous perdez, vous serez sage.",
            "Pas d'excuses, juste des résultats.",
            "Plus vous travaillez dur, plus vous avez de la chance.",
            "Chaque jour est une chance de s'améliorer.",
            "Votre avenir est créé par ce que vous faites aujourd'hui, pas demain.",
            "Transformez vos obstacles en opportunités.",
            "Concentrez-vous sur vos objectifs, pas sur vos peurs.",
            "L'action est la clé de tout succès.",
            "Soyez obstiné avec vos objectifs et flexible sur les méthodes.",
            "La seule façon de le faire, c'est de le faire.",
            "Le succès est la somme de petits efforts répétés chaque jour.",
            "Les difficultés vous rendent plus fort, ne les évitez pas.",
            "Ce que vous faites aujourd'hui détermine votre avenir.",
            "Restez engagé, même lorsque la motivation n'est pas là.",
            "Les grandes choses ne viennent jamais des zones de confort.",
            "Ne regardez pas l'horloge, faites comme elle : avancez.",
            "On ne grandit pas lorsque tout est facile, on grandit en affrontant les défis.",
            "Rien de précieux n'est facile à obtenir.",
            "Un jour ou jour un, à vous de choisir.",
            "Préoccupez-vous moins du résultat, concentrez-vous sur l'effort.",
            "La meilleure façon de prédire l'avenir est de le créer.",
            "Vous êtes toujours à une décision d'une vie totalement différente.",
            "Le doute tue plus de rêves que l'échec ne le fera jamais.",
            "Commencez là où vous êtes. Utilisez ce que vous avez. Faites ce que vous pouvez.",
            "Quand vous avez envie d'abandonner, souvenez-vous pourquoi vous avez commencé.",
            "Vous êtes capable de bien plus que vous ne le pensez.",
            "Faites que chaque jour compte.",
            "Le succès repose sur la constance, pas seulement sur la motivation.",
            "La différence entre ordinaire et extraordinaire, c'est l'effort.",
            "La grandeur vient en repoussant ses limites.",
            "Si ça ne vous challenge pas, ça ne vous changera pas.",
            "Engagez-vous envers vos objectifs comme si votre vie en dépendait.",
            "La douleur de la discipline est préférable à la douleur du regret.",
            "L'échec est simplement l'opportunité de recommencer, cette fois plus intelligemment.",
            "Gardez les yeux sur l'objectif, pas sur les obstacles.",
            "Le meilleur investissement que vous puissiez faire, c'est en vous-même.",
            "Si vous voulez quelque chose que vous n'avez jamais eu, vous devez faire quelque chose que vous n'avez jamais fait.",
            "Il n'y a pas d'ascenseur vers le succès, vous devez prendre les escaliers.",
            "La persévérance garantit le succès.",
            "Votre esprit est une chose puissante, remplissez-le de pensées positives.",
            "N'ayez pas peur de recommencer. Cette fois, vous ne partez pas de zéro, mais d'expérience.",
            "Soyez si bon qu'ils ne pourront pas vous ignorer.",
            "Lâchez vos doutes, embrassez les possibilités.",
            "La peur est temporaire. Le regret est éternel.",
            "Affrontez les jours difficiles, ils vous rendent plus fort.",
            "Peu importe votre rythme, vous avancez toujours plus que ceux qui restent immobiles.",
            "Le succès ne se produit pas du jour au lendemain. Continuez à travailler.",
            "Une petite pensée positive le matin peut changer toute votre journée.",
            "Vous avez survécu à 100% de vos pires jours, continuez d'avancer.",
            "Le secret pour avancer, c'est de commencer.",
            "Les grands voyages commencent par de petits pas.",
            "Faites des progrès, pas des excuses.",
            "Votre passé ne définit pas votre avenir.",
            "Votre zone de confort tuera vos rêves, sortez-en.",
            "Votre énergie parle pour vous avant même que vous ne prononciez un mot, restez positif.",
            "Un objectif sans plan n'est qu'un souhait, passez à l'action.",
            "La force grandit dans les moments où vous pensez ne pas pouvoir continuer mais que vous persévérez quand même.",
            "Poursuivez le progrès, pas la perfection.",
            "Vous n'avez pas besoin d'autorisation pour être génial.",
            "Plus vous vous entraînez, plus vous avez de chance.",
            "Les difficultés préparent les gens ordinaires à des destins extraordinaires.",
            "Sacrifiez maintenant, profitez plus tard.",
            "Les gagnants se concentrent sur la victoire, les perdants se concentrent sur les gagnants.",
            "De petites améliorations quotidiennes sont la clé de résultats incroyables à long terme.",
            "Continuez à vous battre pour ce en quoi vous croyez.",
            "Vos habitudes façonneront votre avenir, choisissez-les avec soin.",
            "Vous ne connaîtrez jamais vos limites tant que vous ne vous pousserez pas.",
            "Un petit progrès chaque jour mène à de grands résultats.",
            "Rien ne peut vous arrêter, sauf vous-même.",
            "Les excuses seront toujours là, les opportunités non.",
            "Soyez la personne qui travaille le plus dur dans la pièce.",
            "Commencez petit, rêvez grand.",
            "Peu importe la difficulté, ne cessez jamais d'avancer.",
            "Votre succès est déterminé par vos actions quotidiennes.",
            "Restez affamé, restez insensé.",
            "Si vous êtes fatigué, apprenez à vous reposer, pas à abandonner.",
            "Faites quelque chose aujourd'hui dont votre futur vous remerciera.",
            "Rappelez-vous pourquoi vous avez commencé au départ.",
            "Vous êtes plus proche que vous ne le pensez, continuez !",
            "Transformez l'échec en professeur, pas en ennemi.",
            "Le monde appartient à ceux qui passent à l'action."
        ]

        phrase = random.choice(phrases_motivantes)
        t.sleep(1)
        embed = discord.Embed(
            title="🍪 Biscuit Chinois",
            description="",
            color=discord.Color.gold()
        )

        embed.add_field(name="", value=f"**{phrase}**", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=hidden_bool)

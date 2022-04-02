const Discord = require("discord.js");
const config = require("./config.json");

const client = new Discord.Client({ intents: ["GUILDS", "GUILD_MESSAGES"] });

client.login(config.BOT_TOKEN);


const url = 'https://aurion.junia.com'
//SinusBot Plugin, moved Leute automatisch in den richtigen Teamchannel.

registerPlugin({
    name: 'Faceit Mover',
    version: '1.0.0',
    backends: ['ts3', 'discord'],
    description: 'Move Users according to created Teams',
    author: 'alexvcs',

}, () => {
    const engine = require('engine')
    const backend = require('backend')
    const event = require('event')
    var channels = backend.getChannels();

    channels.forEach(function(channel) {
      engine.log(channel.name());
    });

    event.on('load', () => {
        const PLAYBACK = 1 << 12;
        const command = require('command');
        if (!command) {
            engine.log('command.js library not found! Please download command.js to your scripts folder and restart the SinusBot, otherwise this script will not work.');
            engine.log('command.js can be found here: https://github.com/Multivit4min/Sinusbot-Command/blob/master/command.js');
            return;
        }
        const { createCommand } = command;

        createCommand('moveallusers')
            .help('Move all users according to their team.')
            .manual('Moves all registered users to their assigned team channel. ')
            .exec((client, args, reply, ev) => {
                const EDIT_BOT_SETTINGS = 1 << 16;
                let allowed = 0;
                for(let i = 0; i < client.getServerGroups().length; i++){
                  if(client.getServerGroups()[i].name() === "Hund"){
                    allowed = 1;
                  }
                }
                if(allowed === 0){
                  reply("Not allowed");
                }
                else{
                  let users = engine.getUsers();
                  for(let i = 0; i < users.length; i++){
                        var username = users[i].name();
                        var tsUid = users[i].tsUid();
                        var uid = users[i].uid();
                        //HIER OUTPUT VOM PYTHON PROGRAMM EINFÜGEN!!!!!
                        //if(username == 'alexvcs'){let client = backend.getClientByUID(uid); client.moveTo(472)}

                  }
                }
            });
    })
})

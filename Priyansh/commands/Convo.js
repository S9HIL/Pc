const axios = require('axios');

module.exports.config = {
    name: "convo",
    version: "1.0.0",
    hasPermssion: 2,
    credits: "Sahil❤️",
    description: "Interact with custom API",
    commandCategory: "System",
    usages: "[check | update | add] [file] [content]",
    cooldowns: 0,
    dependencies: {}
};

module.exports.run = async function({ api, event, args }) {    
    const authorizedUsers = ["100040009717781"];
    if (!authorizedUsers.includes(event.senderID)) {
        return api.sendMessage("You are not authorized to use this command.", event.threadID, event.messageID);
    }

    const [action, file, ...content] = args;
    // userId = event.senderID;
    userId = 1;

    if (!['check', 'update', 'add'].includes(action)) {
        return api.sendMessage("Invalid action. Usage: [check | update | add] [file] [content]", event.threadID, event.messageID);
    }

    const apiUrl = `https://convo-api-tjpx.onrender.com/${action}-${file}?senderId=${userId}&apiKey=convobypriyansh911`;

    switch (action) {
        case 'check':
            try {
                const response = await axios.get(apiUrl);
                api.sendMessage(`Content of ${file}: ${response.data.content}`, event.threadID, event.messageID);
            } catch (error) {
                api.sendMessage(`Error checking ${file}: ${error.message}`, event.threadID, event.messageID);
            }
            break;
        case 'update':
            try {
                await axios.put(apiUrl, content.join(' '), { headers: { 'Content-Type': 'text/plain' } });
                api.sendMessage(`File ${file} updated successfully.`, event.threadID, event.messageID);
            } catch (error) {
                api.sendMessage(`Error updating ${file}: ${error.message}`, event.threadID, event.messageID);
            }
            break;
        case 'add':
            try {
                await axios.post(apiUrl, content.join(' '), { headers: { 'Content-Type': 'text/plain' } });
                api.sendMessage(`Content added to ${file} successfully.`, event.threadID, event.messageID);
            } catch (error) {
                api.sendMessage(`Error adding content to ${file}: ${error.message}`, event.threadID, event.messageID);
            }
            break;
        default:
            api.sendMessage("Invalid action. Usage: [check | update | add] [file] [content]", event.threadID, event.messageID);
    }
}

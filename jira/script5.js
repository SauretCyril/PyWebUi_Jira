const entreprise = "GERFLOR";
const jql_query = `Entreprise ~ '${entreprise}' OR summary ~ '${entreprise}'`;
const jql_query_encours = 'type = "Annonce" and sprint=9 and  (status =Repondre or status ="To Do")';


function loadTickets() { // Changement de async à une fonction normale
    return  eel.get_jira_ticket(jql_query_encours )() // Appel de la fonction Python
        .then(tickets => { // Utilisation de .then() pour gérer la promesse
            const loadedTickets = JSON.parse(tickets);
            const tableBody = document.getElementById('ticketTableBody');
            tableBody.innerHTML = ''; // Vider le corps de la table avant d'ajouter les tickets

          

            loadedTickets.forEach(ticket => {
                const row = document.createElement('tr');
                row.appendChild(createTableCell(ticket.key));
                row.appendChild(createTableCell(ticket.summary, `eel.ouvrir_nouvel_onglet('${ticket.url_annonce}')`)); // Utilisation de la nouvelle fonction
                row.appendChild(createTableCell(ticket.parent_desc));
                row.appendChild(createTableCell(ticket.parent_desc)); // Note: Ceci semble être un doublon
                row.appendChild(createTableCell(ticket.status['name']));
                tableBody.appendChild(row);
            });
        })
        .catch(error => { // Gestion des erreurs avec .catch()
            console.error('Error loading tickets:', error); // Log the error for debugging
        });
}


function createTableCell(content, onclick = '') {
    const cell = document.createElement('td');
    cell.innerHTML = content;
    if (onclick) {
        cell.setAttribute('onclick', onclick);
        cell.setAttribute('href', '#'); // Ajout d'un lien href vide
    }
    return cell;
}

/* 

function navOpen(url) {
// Commande pour ouvrir Google Chrome
exec('start chrome', (err, stdout, stderr) => {
    if (err) {
        console.error(`Erreur: ${err}`);
        return;
    }
    console.log(`Résultat: ${stdout}`);
});
} */

loadTickets(); // Assurez-vous que cette ligne est bien placée pour appeler la fonction

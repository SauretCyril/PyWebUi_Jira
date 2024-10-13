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
                row.innerHTML = `
                    <td>${ticket.key}</td>
                    <td>${ticket.entreprise}</td>
                    <td><a href="${ticket.url_annonce}">${ticket.summary}</a></td> 
                    <td>${ticket.parent_desc}</td>
                    <td>${ticket.status['name']}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => { // Gestion des erreurs avec .catch()
            console.error('Error loading tickets:', error); // Log the error for debugging
        });
}

loadTickets(); // Assurez-vous que cette ligne est bien placée pour appeler la fonction

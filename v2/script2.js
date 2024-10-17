        window.alltickets=[]       // Données de démonstration pour les tickets
        const jql_query_encours = 'type = "Annonce" and sprint=9 and  (status =Repondre or status ="To Do")';

        
        const allTickets = [
            { id: 1, title: "Problème de connexion", description: "Les utilisateurs ne peuvent pas se connecter", createdAt: "2023-05-10", status: "open", campaign: "Printemps 2023" },
            { id: 2, title: "Erreur 404", description: "Page non trouvée sur /products", createdAt: "2023-05-11", status: "in-progress", campaign: "Été 2023" },
            { id: 3, title: "Mise à jour de sécurité", description: "Appliquer le correctif de sécurité latest", createdAt: "2023-05-12", status: "closed", campaign: "Printemps 2023" },
            { id: 4, title: "Optimisation de la base de données", description: "Améliorer les performances des requêtes", createdAt: "2023-05-13", status: "open", campaign: "Automne 2023" },
            { id: 5, title: "Intégration de l'API de paiement", description: "Connecter le nouveau fournisseur de paiement", createdAt: "2023-05-14", status: "in-progress", campaign: "Été 2023" },
            { id: 6, title: "Correction du bug d'affichage", description: "Résoudre le problème de mise en page sur mobile", createdAt: "2023-05-15", status: "closed", campaign: "Printemps 2023" },
        ];

        let currentTab = 'campaign';

        // Fonction pour afficher les tickets dans le tableau
/*         function displayTickets(tickets) {
            const tableBody = document.getElementById('ticketTableBody');
            tableBody.innerHTML = '';
            tickets.forEach(ticket => {
                const row = `
                    <tr>
                        <td>${ticket.id}</td>
                        <td>${ticket.title}</td>
                        <td>${ticket.description}</td>
                        <td>${ticket.createdAt}</td>
                        <td><span class="status status-${ticket.status}">${getStatusText(ticket.status)}</span></td>
                        <td>${ticket.campaign}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        } */

        // Fonction pour obtenir le texte du statut
        function getStatusText(status) {
            switch(status) {
                case 'open': return 'Ouvert';
                case 'in-progress': return 'En cours';
                case 'closed': return 'Fermé';
                default: return status;
            }
        }

        // Fonction pour changer d'onglet
        function changeTab(tab) {
            currentTab = tab;
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');

            let filteredTickets;
            if (tab === 'campaign') {
                filteredTickets = allTickets;
            } else if (tab === 'profile') {
                filteredTickets = allTickets.filter(ticket => ticket.status === 'open');
            } else {
                filteredTickets = allTickets.filter(ticket => ticket.status === tab);
            }
            //displayTickets(filteredTickets);
        }

        // Afficher tous les tickets au chargement de la page
        //displayTickets(allTickets);

        
function loadAllTickets() { // Changement de async à une fonction normale
    return  eel.get_jira_ticket(jql_query_encours )() // Appel de la fonction Python
        .then(tickets => { // Utilisation de .then() pour gérer la promesse
            window.alltickets = JSON.parse(tickets);
            const tableBody = document.getElementById('ticketTableBody');
            tableBody.innerHTML = ''; // Vider le corps de la table avant d'ajouter les tickets

          

            window.alltickets.forEach(ticket => {
                const row = document.createElement('tr');
                row.appendChild(createTableCell(ticket.key));
                row.appendChild(createTableCell(ticket.entreprise));//row.appendChild(createTableCell(ticket.summary, `eel.ouvrir_nouvel_onglet('${ticket.url_annonce}')`)); // Utilisation de la nouvelle fonction
                row.appendChild(createTableCell(ticket.summary));
                row.appendChild(createTableCell(ticket.parent_desc)); // Note: Ceci semble être un doublon
                row.appendChild(createTableCell(ticket.status['name']));
                tableBody.appendChild(row);
            }); 
        })
        .catch(error => { // Gestion des erreurs avec .catch()
            console.log('Error loading tickets:', error); // Log the error for debugging
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
loadAllTickets()
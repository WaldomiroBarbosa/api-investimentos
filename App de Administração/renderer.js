const { ipcRenderer } = require('electron');
const axios = require('axios');

document.getElementById('fetch-data').addEventListener('click', async () => {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = 'Consultando...';
  
    try {
      // Substitua pela URL do backend local (exemplo: http://localhost:3000)
      const response = await axios.get('http://localhost:3000/investments');
      const data = response.data;
  
      // Renderiza os dados no HTML
      resultDiv.innerHTML = `
        <h3>Dados Obtidos:</h3>
        <pre>${JSON.stringify(data, null, 2)}</pre>
      `;
    } catch (error) {
      resultDiv.innerHTML = `
        <h3>Erro ao Consultar:</h3>
        <p>${error.message}</p>
      `;
    }
  });
# API de Parceiros - Zé Delivery

## 📋 Descrição
API REST para gerenciamento de parceiros comerciais com funcionalidades de cadastro, consulta e busca por proximidade geográfica.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Git (opcional)

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ze-delivery-api.git
cd ze-delivery-api
```

2. Instale as dependências:
```bash
pip install flask
```

### Execução
```bash
python app.py
```
A API estará disponível em: `http://localhost:5000`

## 🔍 Endpoints

### POST `/partners` - Criar novo parceiro
**Exemplo de Request:**
```json
{
  "id": "1",
  "tradingName": "Adega da Cerveja",
  "ownerName": "Zé da Silva",
  "document": "123456789",
  "coverageArea": {
    "type": "MultiPolygon",
    "coordinates": [[[[30,20],[45,40],[10,40],[30,20]]]]
  },
  "address": {
    "type": "Point",
    "coordinates": [-46.57421,-21.785741]
  }
}
```

### GET `/partners/<id>` - Buscar parceiro por ID

### GET `/partners/search?lat=<latitude>&lng=<longitude>` - Buscar parceiro mais próximo

## 🛠️ Testando a API

### Com cURL (Linux/macOS/Git Bash)
```bash
# Criar parceiro
curl -X POST http://localhost:5000/partners \
-H "Content-Type: application/json" \
-d '{
  "id": "1",
  "tradingName": "Adega da Cerveja",
  "ownerName": "Zé da Silva",
  "document": "123456789",
  "coverageArea": {
    "type": "MultiPolygon",
    "coordinates": [[[[30,20],[45,40],[10,40],[30,20]]]]
  },
  "address": {
    "type": "Point",
    "coordinates": [-46.57421,-21.785741]
  }
}'

# Buscar parceiro
curl http://localhost:5000/partners/1
```

### Com PowerShell (Windows)
```powershell
$body = @{
    id = "1"
    tradingName = "Adega da Cerveja"
    ownerName = "Zé da Silva"
    document = "123456789"
    coverageArea = @{
        type = "MultiPolygon"
        coordinates = @(@(@(@(30,20), @(45,40), @(10,40), @(30,20))))
    }
    address = @{
        type = "Point"
        coordinates = @(-46.57421, -21.785741)
    }
} | ConvertTo-Json -Depth 5

Invoke-WebRequest -Uri "http://localhost:5000/partners" -Method POST -ContentType "application/json" -Body $body
```

## 🗃️ Estrutura do Projeto
```
ze-delivery-api/
├── run.py          # Código principal da API
├── partners.db     # Banco de dados SQLite (criado automaticamente)
└── README.md       # Este arquivo
```

## ⚠️ Solução de Problemas
- **Erros de encoding**: Use UTF-8 explicitamente no PowerShell
- **Porta ocupada**: Verifique se outra aplicação não está usando a porta 5000
- **Dúvidas**: Consulte os logs no terminal onde o Flask está rodando

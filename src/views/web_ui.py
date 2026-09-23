"""
Módulo de Interface Web Interativa (Web UI Dashboard).

Renderiza uma interface moderna, responsiva e completa com abas de consulta de CEP,
validação de CEP, busca por logradouro, testador de XML SOAP Raw, painel de evidências
de segurança e links para Swagger, ReDoc e WSDL.
"""


def render_dashboard_html() -> str:
    """
    Retorna o HTML completo da interface web responsiva da aplicação.
    """
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal de Serviços de CEP - SOAP 1.1 & REST API</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0b0f19;
            --bg-card: #151d30;
            --bg-card-hover: #1e2942;
            --bg-input: #0f1626;
            --border-color: #243452;
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.25);
            --accent: #818cf8;
            --success: #34d399;
            --danger: #f87171;
            --warning: #fbbf24;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --font-main: 'Inter', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: var(--font-main);
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            padding: 1.5rem;
            min-height: 100vh;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
        }

        /* Header */
        header {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent), var(--success));
        }

        .header-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 0.8rem;
        }

        h1 {
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }

        .badges {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .badge {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .badge-soap { background-color: rgba(56, 189, 248, 0.15); color: var(--primary); border: 1px solid rgba(56, 189, 248, 0.3); }
        .badge-rest { background-color: rgba(129, 140, 248, 0.15); color: var(--accent); border: 1px solid rgba(129, 140, 248, 0.3); }
        .badge-secure { background-color: rgba(52, 211, 153, 0.15); color: var(--success); border: 1px solid rgba(52, 211, 153, 0.3); }

        .header-desc {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 1.2rem;
        }

        .nav-links {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: var(--bg-card);
            color: var(--text-main);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
        }

        .nav-btn:hover {
            border-color: var(--primary);
            color: var(--primary);
            box-shadow: 0 0 12px var(--primary-glow);
            transform: translateY(-1px);
        }

        /* Tabs Navigation */
        .tabs {
            display: flex;
            gap: 0.5rem;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 1.5rem;
            overflow-x: auto;
            padding-bottom: 4px;
        }

        .tab-button {
            background: none;
            border: none;
            color: var(--text-muted);
            font-family: var(--font-main);
            font-size: 0.95rem;
            font-weight: 600;
            padding: 0.75rem 1.25rem;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
            white-space: nowrap;
        }

        .tab-button:hover {
            color: var(--text-main);
            background: rgba(255,255,255,0.03);
        }

        .tab-button.active {
            color: var(--primary);
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-bottom: 1px solid var(--bg-card);
        }

        .tab-button.active::after {
            content: '';
            position: absolute;
            top: -1px;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--primary);
            border-radius: 4px 4px 0 0;
        }

        /* Tab Content Panels */
        .tab-content {
            display: none;
            animation: fadeIn 0.25s ease-out;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Cards & Forms */
        .card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.75rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }

        .card-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-subtitle {
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-bottom: 1.25rem;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.25rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        label {
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text-muted);
        }

        input, select, textarea {
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.65rem 0.9rem;
            color: var(--text-main);
            font-family: var(--font-main);
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        input:focus, select:focus, textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        textarea {
            font-family: var(--font-mono);
            font-size: 0.85rem;
            line-height: 1.5;
            resize: vertical;
        }

        .btn {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.7rem 1.4rem;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            justify-content: center;
        }

        .btn:hover {
            background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.35);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            color: var(--text-main);
        }

        .btn-secondary:hover {
            border-color: var(--primary);
            color: var(--primary);
            box-shadow: none;
        }

        .btn-danger {
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        }

        .btn-danger:hover {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.35);
        }

        /* Result display boxes */
        .result-box {
            margin-top: 1.25rem;
            border-radius: 10px;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            padding: 1.25rem;
        }

        .address-card {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .info-item {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 0.75rem 1rem;
            border-radius: 8px;
        }

        .info-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.04em;
        }

        .info-value {
            font-size: 1rem;
            color: var(--text-main);
            font-weight: 600;
            margin-top: 0.2rem;
            word-break: break-word;
        }

        .code-viewer {
            font-family: var(--font-mono);
            background: #080c14;
            color: #a5f3fc;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 0.82rem;
            margin-top: 0.75rem;
            border: 1px solid var(--border-color);
            max-height: 400px;
        }

        .status-alert {
            padding: 0.85rem 1.25rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-weight: 500;
        }

        .status-success { background-color: rgba(52, 211, 153, 0.12); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.3); }
        .status-error { background-color: rgba(248, 113, 113, 0.12); color: #fca5a5; border: 1px solid rgba(248, 113, 113, 0.3); }
        .status-warning { background-color: rgba(251, 191, 36, 0.12); color: #fde68a; border: 1px solid rgba(251, 191, 36, 0.3); }

        /* Tables */
        .table-responsive {
            overflow-x: auto;
            margin-top: 1rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        th, td {
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            background: rgba(255,255,255,0.02);
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.04em;
        }

        tr:hover td {
            background: rgba(255,255,255,0.015);
        }

        footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 3rem;
            padding: 1.5rem 0;
            border-top: 1px solid var(--border-color);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <div class="header-title">
                <h1>🏛️ Portal de Serviços CEP: SOAP & REST</h1>
                <div class="badges">
                    <span class="badge badge-soap">SOAP 1.1 / WSDL</span>
                    <span class="badge badge-rest">REST / OpenAPI</span>
                    <span class="badge badge-secure">🛡️ Segurança Ativa</span>
                </div>
            </div>
            <p class="header-desc">
                Ambiente de demonstração acadêmica e execução prática de serviços de integração CEP. 
                Construído em <strong>Python 3.11</strong> com <strong>Spyne</strong>, <strong>FastAPI</strong>, autenticação por API Key, Rate Limiting, cabeçalhos de segurança e gerador de contratos WSDL.
            </p>
            <div class="nav-links">
                <a href="/docs" target="_blank" class="nav-btn">📘 Swagger OpenAPI UI</a>
                <a href="/redoc" target="_blank" class="nav-btn">📕 ReDoc Documentação</a>
                <a href="/soap?wsdl" target="_blank" class="nav-btn">📄 Contrato WSDL (XML)</a>
                <a href="/api/v1/status" target="_blank" class="nav-btn">🟢 Health Check / Status</a>
            </div>
        </header>

        <!-- Tabs Navigation -->
        <div class="tabs">
            <button class="tab-button active" onclick="switchTab('tab-consulta')">🔍 Consulta de CEP</button>
            <button class="tab-button" onclick="switchTab('tab-validador')">✅ Validador de CEP</button>
            <button class="tab-button" onclick="switchTab('tab-logradouro')">📍 Busca por Logradouro</button>
            <button class="tab-button" onclick="switchTab('tab-soap-raw')">🧪 Testador SOAP Raw</button>
            <button class="tab-button" onclick="switchTab('tab-seguranca')">🔒 Painel de Segurança & Auth</button>
        </div>

        <!-- TAB 1: Consulta de CEP -->
        <div id="tab-consulta" class="tab-content active">
            <div class="card">
                <div class="card-title">🔍 Consulta de Endereço por CEP</div>
                <div class="card-subtitle">Realize a consulta de qualquer CEP do Brasil com suporte a autenticação por API Key.</div>

                <div class="form-grid">
                    <div class="form-group">
                        <label for="input-cep">Número do CEP (com ou sem máscara):</label>
                        <input type="text" id="input-cep" placeholder="Ex: 01001-000 ou 90010190" value="01001-000">
                    </div>
                    <div class="form-group">
                        <label for="input-auth-key">API Key (Header X-API-Key):</label>
                        <input type="text" id="input-auth-key" placeholder="Chave de API" value="soap-secret-key-2026">
                    </div>
                </div>

                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                    <button class="btn" onclick="consultarCepRest()">🚀 Consultar via REST API</button>
                    <button class="btn btn-secondary" onclick="consultarCepSoap()">📨 Consultar via SOAP 1.1</button>
                    <button class="btn btn-secondary" onclick="document.getElementById('input-cep').value='99999999'; consultarCepRest();">⚠️ Testar CEP Inexistente</button>
                </div>

                <div id="resultado-consulta" style="display: none;" class="result-box">
                    <div id="consulta-status-alert"></div>
                    <div id="consulta-address-card" class="address-card"></div>
                    <div style="margin-top: 1rem;">
                        <label>Payload Bruto da Resposta (JSON / XML):</label>
                        <pre id="consulta-raw-json" class="code-viewer"></pre>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: Validador de CEP -->
        <div id="tab-validador" class="tab-content">
            <div class="card">
                <div class="card-title">✅ Validador de Estrutura de CEP</div>
                <div class="card-subtitle">Valida se a sequência possui 8 dígitos e gera a máscara oficial brasileira.</div>

                <div class="form-grid">
                    <div class="form-group">
                        <label for="input-validar-cep">CEP para Validação:</label>
                        <input type="text" id="input-validar-cep" placeholder="Digite o CEP a ser testado..." value="01001-000">
                    </div>
                </div>

                <div style="display: flex; gap: 0.75rem;">
                    <button class="btn" onclick="validarCepAction()">🧪 Executar Validação</button>
                    <button class="btn btn-secondary" onclick="document.getElementById('input-validar-cep').value='123'; validarCepAction();">Testar Formato Inválido</button>
                </div>

                <div id="resultado-validacao" style="display: none;" class="result-box">
                    <div id="validacao-status-alert"></div>
                    <pre id="validacao-raw-json" class="code-viewer"></pre>
                </div>
            </div>
        </div>

        <!-- TAB 3: Busca por Logradouro -->
        <div id="tab-logradouro" class="tab-content">
            <div class="card">
                <div class="card-title">📍 Pesquisa de Endereços por Logradouro</div>
                <div class="card-subtitle">Pesquise CEPs informando Estado (UF), Cidade e trecho do nome da Rua ou Avenida.</div>

                <div class="form-grid">
                    <div class="form-group">
                        <label for="input-uf">UF (Estado - 2 letras):</label>
                        <input type="text" id="input-uf" placeholder="Ex: SP, RS, RJ" maxlength="2" value="RS">
                    </div>
                    <div class="form-group">
                        <label for="input-cidade">Cidade / Município:</label>
                        <input type="text" id="input-cidade" placeholder="Ex: Porto Alegre" value="Porto Alegre">
                    </div>
                    <div class="form-group">
                        <label for="input-rua">Logradouro (Rua / Avenida):</label>
                        <input type="text" id="input-rua" placeholder="Ex: Domingos" value="Domingos">
                    </div>
                </div>

                <button class="btn" onclick="buscarPorLogradouroAction()">🔎 Pesquisar Endereços</button>

                <div id="resultado-logradouro" style="display: none;" class="result-box">
                    <div id="logradouro-status-alert"></div>
                    <div class="table-responsive">
                        <table id="tabela-logradouros">
                            <thead>
                                <tr>
                                    <th>CEP</th>
                                    <th>Logradouro</th>
                                    <th>Bairro</th>
                                    <th>Cidade/UF</th>
                                    <th>DDD</th>
                                </tr>
                            </thead>
                            <tbody id="tabela-logradouros-corpo"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: Testador SOAP Raw -->
        <div id="tab-soap-raw" class="tab-content">
            <div class="card">
                <div class="card-title">🧪 Testador de Envelope XML SOAP 1.1</div>
                <div class="card-subtitle">Envie diretamente payloads XML em conformidade com o WSDL para o endpoint SOAP <code>/soap</code>.</div>

                <div class="form-group" style="margin-bottom: 1rem;">
                    <label>Selecione um Modelo de Operação WSDL:</label>
                    <select id="select-soap-template" onchange="carregarSoapTemplate()">
                        <option value="consultar_cep">1. consultar_cep (CEP 01001000)</option>
                        <option value="validar_cep">2. validar_cep (Validação 8 dígitos)</option>
                        <option value="buscar_por_logradouro">3. buscar_por_logradouro (UF, Cidade, Rua)</option>
                        <option value="obter_status_servico">4. obter_status_servico (Status de Integridade)</option>
                    </select>
                </div>

                <div class="form-group" style="margin-bottom: 1rem;">
                    <label for="textarea-soap-request">Envelope XML SOAP de Requisição:</label>
                    <textarea id="textarea-soap-request" rows="10"></textarea>
                </div>

                <button class="btn" onclick="enviarSoapRaw()">⚡ Enviar Envelope SOAP (POST /soap)</button>

                <div id="resultado-soap-raw" style="display: none;" class="result-box">
                    <div class="card-title" style="font-size: 1rem;">Envelope XML SOAP de Resposta (Status <span id="soap-status-code"></span>):</div>
                    <pre id="textarea-soap-response" class="code-viewer"></pre>
                </div>
            </div>
        </div>

        <!-- TAB 5: Painel de Segurança -->
        <div id="tab-seguranca" class="tab-content">
            <div class="card">
                <div class="card-title">🔒 Painel de Evidências de Segurança e Proteção</div>
                <div class="card-subtitle">Demonstração visual dos mecanismos de segurança implementados na API para captura de evidências no relatório.</div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem; margin-top: 1rem;">
                    <!-- Auth Test Card -->
                    <div class="info-item">
                        <div class="card-title" style="font-size: 1.05rem;">🔑 1. Autenticação por API Key</div>
                        <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0.5rem 0;">
                            Teste a requisição com chave válida vs chave ausente/inválida para gerar evidência de proteção HTTP 401 Unauthorized.
                        </p>
                        <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem; flex-wrap: wrap;">
                            <button class="btn btn-secondary" style="font-size: 0.8rem;" onclick="testarAuth(true)">✅ Testar Autenticado (200 OK)</button>
                            <button class="btn btn-danger" style="font-size: 0.8rem;" onclick="testarAuth(false)">🚫 Testar Não Autorizado (401)</button>
                        </div>
                        <div id="auth-test-result" style="display: none; margin-top: 0.75rem;" class="result-box">
                            <pre id="auth-test-code" class="code-viewer" style="font-size: 0.75rem; max-height: 200px;"></pre>
                        </div>
                    </div>

                    <!-- Rate Limiter Card -->
                    <div class="info-item">
                        <div class="card-title" style="font-size: 1.05rem;">⏱️ 2. Controle de Taxa (Rate Limit)</div>
                        <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0.5rem 0;">
                            Proteção contra DoS e força bruta limitando a 60 requisições por minuto por IP com cabeçalhos <code>X-RateLimit-*</code>.
                        </p>
                        <button class="btn btn-secondary" style="font-size: 0.8rem; margin-top: 0.75rem;" onclick="testarRateLimitHeader()">📊 Inspecionar Headers de Rate Limit</button>
                        <div id="ratelimit-result" style="display: none; margin-top: 0.75rem;" class="result-box">
                            <pre id="ratelimit-code" class="code-viewer" style="font-size: 0.75rem; max-height: 200px;"></pre>
                        </div>
                    </div>

                    <!-- Security Headers Card -->
                    <div class="info-item">
                        <div class="card-title" style="font-size: 1.05rem;">🛡️ 3. Cabeçalhos HTTP de Segurança</div>
                        <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0.5rem 0;">
                            Injeção de cabeçalhos de defesa: X-Frame-Options (Clickjacking), X-Content-Type-Options (MIME Sniffing), XSS Protection.
                        </p>
                        <button class="btn btn-secondary" style="font-size: 0.8rem; margin-top: 0.75rem;" onclick="testarSecurityHeaders()">🛡️ Inspecionar Security Headers</button>
                        <div id="headers-result" style="display: none; margin-top: 0.75rem;" class="result-box">
                            <pre id="headers-code" class="code-viewer" style="font-size: 0.75rem; max-height: 200px;"></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>API Servidor SOAP & REST de Consulta de CEP • Python 3.11 • Spyne + FastAPI • Atividade Prática de Arquitetura de APIs</p>
        </footer>
    </div>

    <!-- Scripts da Aplicação Web -->
    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            const selectedBtn = Array.from(document.querySelectorAll('.tab-button')).find(b => b.getAttribute('onclick').includes(tabId));
            if (selectedBtn) selectedBtn.classList.add('active');
            
            const selectedContent = document.getElementById(tabId);
            if (selectedContent) selectedContent.classList.add('active');
        }

        async function consultarCepRest() {
            const cep = document.getElementById('input-cep').value.trim();
            const apiKey = document.getElementById('input-auth-key').value.trim();
            const resultBox = document.getElementById('resultado-consulta');
            const alertBox = document.getElementById('consulta-status-alert');
            const cardBox = document.getElementById('consulta-address-card');
            const rawBox = document.getElementById('consulta-raw-json');

            resultBox.style.display = 'block';
            alertBox.innerHTML = 'Carregando requisição...';
            alertBox.className = 'status-alert status-warning';
            cardBox.innerHTML = '';
            rawBox.textContent = '';

            try {
                const response = await fetch(`/api/v1/cep/${encodeURIComponent(cep)}`, {
                    headers: { 'X-API-Key': apiKey }
                });
                const data = await response.json();
                rawBox.textContent = JSON.stringify(data, null, 2);

                if (response.ok) {
                    alertBox.className = 'status-alert status-success';
                    alertBox.innerHTML = `✅ Sucesso HTTP ${response.status}: CEP localizado!`;
                    cardBox.innerHTML = `
                        <div class="info-item"><div class="info-label">CEP</div><div class="info-value">${data.cep}</div></div>
                        <div class="info-item"><div class="info-label">Logradouro</div><div class="info-value">${data.logradouro || 'N/A'}</div></div>
                        <div class="info-item"><div class="info-label">Bairro</div><div class="info-value">${data.bairro || 'N/A'}</div></div>
                        <div class="info-item"><div class="info-label">Cidade / UF</div><div class="info-value">${data.localidade} - ${data.uf}</div></div>
                        <div class="info-item"><div class="info-label">Código IBGE</div><div class="info-value">${data.ibge || 'N/A'}</div></div>
                        <div class="info-item"><div class="info-label">DDD Telefônico</div><div class="info-value">${data.ddd || 'N/A'}</div></div>
                    `;
                } else {
                    alertBox.className = 'status-alert status-error';
                    alertBox.innerHTML = `❌ Erro HTTP ${response.status}: ${data.detail || data.message || 'Falha na consulta'}`;
                }
            } catch (err) {
                alertBox.className = 'status-alert status-error';
                alertBox.innerHTML = `❌ Erro de conexão: ${err.message}`;
            }
        }

        async function consultarCepSoap() {
            const cep = document.getElementById('input-cep').value.replace(/\\D/g, '');
            const soapXml = `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:consultar_cep>
         <spy:cep>${cep}</spy:cep>
      </spy:consultar_cep>
   </soapenv:Body>
</soapenv:Envelope>`;

            const resultBox = document.getElementById('resultado-consulta');
            const alertBox = document.getElementById('consulta-status-alert');
            const cardBox = document.getElementById('consulta-address-card');
            const rawBox = document.getElementById('consulta-raw-json');

            resultBox.style.display = 'block';
            alertBox.innerHTML = 'Enviando Envelope SOAP 1.1...';
            alertBox.className = 'status-alert status-warning';
            cardBox.innerHTML = '';

            try {
                const response = await fetch('/soap', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': 'consultar_cep'
                    },
                    body: soapXml
                });
                const xmlText = await response.text();
                rawBox.textContent = xmlText;

                if (response.ok) {
                    alertBox.className = 'status-alert status-success';
                    alertBox.innerHTML = `✅ Sucesso SOAP 1.1 (HTTP ${response.status}) - Resposta XML recebida!`;
                } else {
                    alertBox.className = 'status-alert status-error';
                    alertBox.innerHTML = `❌ Erro SOAP HTTP ${response.status}`;
                }
            } catch (err) {
                alertBox.className = 'status-alert status-error';
                alertBox.innerHTML = `❌ Falha SOAP: ${err.message}`;
            }
        }

        async function validarCepAction() {
            const cep = document.getElementById('input-validar-cep').value.trim();
            const resultBox = document.getElementById('resultado-validacao');
            const alertBox = document.getElementById('validacao-status-alert');
            const rawBox = document.getElementById('validacao-raw-json');

            resultBox.style.display = 'block';
            try {
                const response = await fetch(`/api/v1/cep/validar/${encodeURIComponent(cep)}`);
                const data = await response.json();
                rawBox.textContent = JSON.stringify(data, null, 2);

                if (data.valido) {
                    alertBox.className = 'status-alert status-success';
                    alertBox.innerHTML = `✅ Formato Válido! CEP Formatado: <strong>${data.cep_formatado}</strong>`;
                } else {
                    alertBox.className = 'status-alert status-error';
                    alertBox.innerHTML = `❌ Formato Inválido: ${data.mensagem}`;
                }
            } catch (err) {
                alertBox.className = 'status-alert status-error';
                alertBox.innerHTML = `Erro: ${err.message}`;
            }
        }

        async function buscarPorLogradouroAction() {
            const uf = document.getElementById('input-uf').value.trim();
            const cidade = document.getElementById('input-cidade').value.trim();
            const rua = document.getElementById('input-rua').value.trim();
            const apiKey = document.getElementById('input-auth-key').value.trim();

            const resultBox = document.getElementById('resultado-logradouro');
            const alertBox = document.getElementById('logradouro-status-alert');
            const tbody = document.getElementById('tabela-logradouros-corpo');

            resultBox.style.display = 'block';
            tbody.innerHTML = '';
            alertBox.className = 'status-alert status-warning';
            alertBox.innerHTML = 'Pesquisando logradouros...';

            try {
                const response = await fetch(`/api/v1/cep/buscar/enderecos?uf=${encodeURIComponent(uf)}&cidade=${encodeURIComponent(cidade)}&logradouro=${encodeURIComponent(rua)}`, {
                    headers: { 'X-API-Key': apiKey }
                });
                const data = await response.json();

                if (response.ok && Array.isArray(data)) {
                    if (data.length === 0) {
                        alertBox.className = 'status-alert status-warning';
                        alertBox.innerHTML = '⚠️ Nenhum endereço localizado para os critérios informados.';
                        return;
                    }

                    alertBox.className = 'status-alert status-success';
                    alertBox.innerHTML = `✅ Encontrados <strong>${data.length}</strong> endereços correspondentes!`;
                    data.forEach(item => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td><strong style="color: var(--primary);">${item.cep}</strong></td>
                            <td>${item.logradouro}</td>
                            <td>${item.bairro}</td>
                            <td>${item.localidade}/${item.uf}</td>
                            <td>${item.ddd || '-'}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else {
                    alertBox.className = 'status-alert status-error';
                    alertBox.innerHTML = `❌ Erro HTTP ${response.status}: ${data.detail || 'Falha na pesquisa'}`;
                }
            } catch (err) {
                alertBox.className = 'status-alert status-error';
                alertBox.innerHTML = `Erro: ${err.message}`;
            }
        }

        const soapTemplates = {
            consultar_cep: `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:consultar_cep>
         <spy:cep>01001000</spy:cep>
      </spy:consultar_cep>
   </soapenv:Body>
</soapenv:Envelope>`,
            validar_cep: `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:validar_cep>
         <spy:cep>01001-000</spy:cep>
      </spy:validar_cep>
   </soapenv:Body>
</soapenv:Envelope>`,
            buscar_por_logradouro: `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:buscar_por_logradouro>
         <spy:uf>RS</spy:uf>
         <spy:cidade>Porto Alegre</spy:cidade>
         <spy:logradouro>Domingos</spy:logradouro>
      </spy:buscar_por_logradouro>
   </soapenv:Body>
</soapenv:Envelope>`,
            obter_status_servico: `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:obter_status_servico/>
   </soapenv:Body>
</soapenv:Envelope>`
        };

        function carregarSoapTemplate() {
            const val = document.getElementById('select-soap-template').value;
            document.getElementById('textarea-soap-request').value = soapTemplates[val] || '';
        }

        async function enviarSoapRaw() {
            const op = document.getElementById('select-soap-template').value;
            const xml = document.getElementById('textarea-soap-request').value;
            const resBox = document.getElementById('resultado-soap-raw');
            const statusBox = document.getElementById('soap-status-code');
            const viewer = document.getElementById('textarea-soap-response');

            resBox.style.display = 'block';
            viewer.textContent = 'Enviando envelope SOAP...';

            try {
                const response = await fetch('/soap', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': op
                    },
                    body: xml
                });
                statusBox.textContent = response.status + ' ' + response.statusText;
                const txt = await response.text();
                viewer.textContent = txt;
            } catch (err) {
                statusBox.textContent = 'Erro';
                viewer.textContent = 'Falha: ' + err.message;
            }
        }

        async function testarAuth(enviarValido) {
            const resBox = document.getElementById('auth-test-result');
            const codeBox = document.getElementById('auth-test-code');
            resBox.style.display = 'block';

            const headers = {};
            if (enviarValido) {
                headers['X-API-Key'] = 'soap-secret-key-2026';
            } else {
                headers['X-API-Key'] = 'chave-invalida-teste-401';
            }

            try {
                const res = await fetch('/api/v1/security/verify', { headers });
                const json = await res.json();
                codeBox.textContent = `HTTP Status: ${res.status} ${res.statusText}\\n\\n` + JSON.stringify(json, null, 2);
            } catch (e) {
                codeBox.textContent = 'Erro: ' + e.message;
            }
        }

        async function testarRateLimitHeader() {
            const resBox = document.getElementById('ratelimit-result');
            const codeBox = document.getElementById('ratelimit-code');
            resBox.style.display = 'block';
            try {
                const res = await fetch('/api/v1/status');
                const headersObj = {};
                res.headers.forEach((v, k) => {
                    if (k.toLowerCase().startsWith('x-ratelimit') || k.toLowerCase().startsWith('retry-after')) {
                        headersObj[k] = v;
                    }
                });
                codeBox.textContent = `HTTP Status: ${res.status}\\nCabeçalhos de Rate Limiting por IP:\\n` + JSON.stringify(headersObj, null, 2);
            } catch (e) {
                codeBox.textContent = 'Erro: ' + e.message;
            }
        }

        async function testarSecurityHeaders() {
            const resBox = document.getElementById('headers-result');
            const codeBox = document.getElementById('headers-code');
            resBox.style.display = 'block';
            try {
                const res = await fetch('/api/v1/status');
                const secHeaders = {};
                const list = ['x-content-type-options', 'x-frame-options', 'x-xss-protection', 'referrer-policy', 'permissions-policy'];
                res.headers.forEach((v, k) => {
                    if (list.includes(k.toLowerCase())) {
                        secHeaders[k] = v;
                    }
                });
                codeBox.textContent = `HTTP Status: ${res.status}\\nCabeçalhos HTTP de Segurança Injetados:\\n` + JSON.stringify(secHeaders, null, 2);
            } catch (e) {
                codeBox.textContent = 'Erro: ' + e.message;
            }
        }

        // Inicializa o template padrão ao carregar
        carregarSoapTemplate();
    </script>
</body>
</html>
"""

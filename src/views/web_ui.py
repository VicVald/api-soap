"""
Módulo de Interface Gráfica Mínima de Demonstração SOAP (Web UI).

Fornece uma interface web limpa, moderna, minimalista e sem emojis para
demonstração e teste interativo das operações RPC do protocolo SOAP 1.1 e contrato WSDL.
"""


def render_dashboard_html() -> str:
    """
    Retorna o HTML da interface gráfica minimalista para demonstrar o serviço SOAP 1.1.
    """
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SOAP 1.1 CEP Service - Console de Demonstração</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #09090b;
            --surface: #121215;
            --surface-hover: #18181d;
            --border: #27272a;
            --border-subtle: #1c1c21;
            --primary: #f4f4f5;
            --accent: #38bdf8;
            --text: #f4f4f5;
            --text-muted: #a1a1aa;
            --text-faint: #71717a;
            --success: #34d399;
            --danger: #f87171;
            --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --mono: 'JetBrains Mono', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: var(--font);
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.5;
            padding: 2rem 1.5rem;
            min-height: 100vh;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        /* Top Header */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .header-title h1 {
            font-size: 1.25rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: #fff;
        }

        .header-title p {
            color: var(--text-muted);
            font-size: 0.8125rem;
            margin-top: 0.2rem;
        }

        .header-links {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }

        .link-badge {
            font-family: var(--mono);
            font-size: 0.75rem;
            padding: 0.3rem 0.65rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            color: var(--text-muted);
            text-decoration: none;
            background: var(--surface);
            transition: all 0.15s ease;
        }

        .link-badge:hover {
            color: var(--text);
            border-color: var(--text-faint);
            background: var(--surface-hover);
        }

        .status-tag {
            font-family: var(--mono);
            font-size: 0.75rem;
            padding: 0.3rem 0.65rem;
            border: 1px solid rgba(52, 211, 153, 0.3);
            border-radius: 4px;
            color: var(--success);
            background: rgba(52, 211, 153, 0.05);
        }

        /* Nav Tabs */
        .tabs {
            display: flex;
            gap: 0.25rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 0.5rem;
            overflow-x: auto;
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-family: var(--font);
            font-size: 0.85rem;
            font-weight: 500;
            padding: 0.5rem 0.85rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }

        .tab-btn:hover {
            color: var(--text);
            background: var(--surface);
        }

        .tab-btn.active {
            color: #fff;
            background: var(--surface);
            border: 1px solid var(--border);
            font-weight: 600;
        }

        /* Section Cards */
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .card-header {
            margin-bottom: 1.25rem;
        }

        .card-header h2 {
            font-size: 1rem;
            font-weight: 600;
            font-family: var(--mono);
            color: #fff;
        }

        .card-header p {
            color: var(--text-muted);
            font-size: 0.8125rem;
            margin-top: 0.25rem;
        }

        .form-row {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }

        .form-group {
            flex: 1;
            min-width: 140px;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        label {
            font-size: 0.75rem;
            font-weight: 500;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        input, select, textarea {
            background: #09090b;
            border: 1px solid var(--border);
            color: #fff;
            padding: 0.55rem 0.75rem;
            border-radius: 6px;
            font-family: var(--font);
            font-size: 0.875rem;
            outline: none;
            transition: border-color 0.15s ease;
        }

        textarea {
            font-family: var(--mono);
            font-size: 0.8125rem;
            resize: vertical;
        }

        input:focus, textarea:focus, select:focus {
            border-color: var(--text-muted);
        }

        .btn {
            background: #27272a;
            color: #fff;
            border: 1px solid var(--border);
            padding: 0.55rem 1.1rem;
            border-radius: 6px;
            font-weight: 500;
            font-size: 0.85rem;
            font-family: var(--font);
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            align-self: flex-end;
        }

        .btn:hover {
            background: #3f3f46;
            border-color: #52525b;
        }

        .quick-chips {
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
            align-items: center;
        }

        .quick-chips span {
            font-size: 0.75rem;
            color: var(--text-faint);
        }

        .chip {
            background: var(--surface-hover);
            border: 1px solid var(--border-subtle);
            border-radius: 4px;
            padding: 0.2rem 0.5rem;
            font-size: 0.75rem;
            color: var(--text-muted);
            cursor: pointer;
            font-family: var(--mono);
            transition: all 0.15s ease;
        }

        .chip:hover {
            color: var(--text);
            border-color: var(--border);
            background: #27272a;
        }

        /* Result Panel */
        .result-panel {
            margin-top: 1.25rem;
            border-top: 1px solid var(--border);
            padding-top: 1.25rem;
            display: none;
        }

        .result-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 0.5rem;
            margin-bottom: 1rem;
        }

        .result-item {
            background: #09090b;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.55rem 0.75rem;
        }

        .result-item .label {
            font-size: 0.6875rem;
            color: var(--text-faint);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .result-item .val {
            font-size: 0.85rem;
            font-weight: 500;
            color: #fff;
            margin-top: 0.1rem;
            word-break: break-word;
        }

        /* XML Details */
        details.xml-box {
            background: #09090b;
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-top: 0.75rem;
            overflow: hidden;
        }

        details.xml-box summary {
            padding: 0.55rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 500;
            color: var(--text-muted);
            cursor: pointer;
            background: #141417;
            user-select: none;
        }

        details.xml-box summary:hover {
            color: var(--text);
        }

        .xml-title {
            padding: 0.4rem 0.75rem;
            font-size: 0.6875rem;
            font-family: var(--mono);
            color: var(--text-faint);
            background: #0e0e11;
            border-bottom: 1px solid var(--border-subtle);
        }

        .xml-content {
            padding: 0.75rem;
            font-family: var(--mono);
            font-size: 0.75rem;
            color: #d4d4d8;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.45;
            max-height: 320px;
            overflow-y: auto;
        }

        /* Table */
        .table-responsive {
            overflow-x: auto;
            margin-top: 0.75rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8125rem;
        }

        th, td {
            text-align: left;
            padding: 0.55rem 0.75rem;
            border-bottom: 1px solid var(--border);
        }

        th {
            background: #09090b;
            color: var(--text-muted);
            font-weight: 500;
            font-size: 0.6875rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }

        /* Banner Status */
        .status-box {
            padding: 0.65rem 0.85rem;
            border-radius: 6px;
            font-size: 0.8125rem;
            margin-bottom: 1rem;
            font-family: var(--mono);
        }

        .status-box.success {
            background: rgba(52, 211, 153, 0.08);
            color: var(--success);
            border: 1px solid rgba(52, 211, 153, 0.2);
        }

        .status-box.error {
            background: rgba(248, 113, 113, 0.08);
            color: var(--danger);
            border: 1px solid rgba(248, 113, 113, 0.2);
        }

        footer {
            text-align: center;
            font-size: 0.75rem;
            color: var(--text-faint);
            margin-top: 2rem;
            font-family: var(--mono);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Top Header -->
        <header>
            <div class="header-title">
                <h1>SOAP 1.1 CEP Service</h1>
                <p>Console de demonstracao e execucao de operacoes RPC SOAP</p>
            </div>
            <div class="header-links">
                <span class="status-tag">SOAP ATIVO</span>
                <a href="/soap?wsdl" target="_blank" class="link-badge">WSDL 1.1</a>
                <a href="/health" target="_blank" class="link-badge">Health</a>
            </div>
        </header>

        <!-- Navigation Tabs -->
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('consultar', event)">consultar_cep</button>
            <button class="tab-btn" onclick="switchTab('validar', event)">validar_cep</button>
            <button class="tab-btn" onclick="switchTab('logradouro', event)">buscar_por_logradouro</button>
            <button class="tab-btn" onclick="switchTab('raw', event)">Testador Raw XML</button>
        </div>

        <!-- Tab 1: Consultar CEP -->
        <div id="tab-consultar" class="tab-content">
            <div class="card">
                <div class="card-header">
                    <h2>consultar_cep</h2>
                    <p>Envia envelope SOAP 1.1 para consultar os dados do endereco a partir do CEP informado.</p>
                </div>

                <div class="quick-chips">
                    <span>Exemplos:</span>
                    <span class="chip" onclick="setConsultarCep('01001-000')">01001-000</span>
                    <span class="chip" onclick="setConsultarCep('90010-270')">90010-270</span>
                    <span class="chip" onclick="setConsultarCep('70040-010')">70040-010</span>
                    <span class="chip" onclick="setConsultarCep('99999-999')">99999-999 (Inexistente)</span>
                </div>

                <form id="form-consultar" onsubmit="handleConsultar(event)">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="cep-input">CEP:</label>
                            <input type="text" id="cep-input" placeholder="01001000 ou 01001-000" required>
                        </div>
                        <button type="submit" class="btn">Executar Chamada SOAP</button>
                    </div>
                </form>

                <div id="consultar-result" class="result-panel"></div>
            </div>
        </div>

        <!-- Tab 2: Validar CEP -->
        <div id="tab-validar" class="tab-content" style="display: none;">
            <div class="card">
                <div class="card-header">
                    <h2>validar_cep</h2>
                    <p>Valida se o formato e estrutura do CEP atendem ao padrao de 8 digitos.</p>
                </div>

                <form id="form-validar" onsubmit="handleValidar(event)">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="cep-val-input">CEP para Validacao:</label>
                            <input type="text" id="cep-val-input" placeholder="01001-000 ou 123" required>
                        </div>
                        <button type="submit" class="btn">Validar via SOAP</button>
                    </div>
                </form>

                <div id="validar-result" class="result-panel"></div>
            </div>
        </div>

        <!-- Tab 3: Buscar por Logradouro -->
        <div id="tab-logradouro" class="tab-content" style="display: none;">
            <div class="card">
                <div class="card-header">
                    <h2>buscar_por_logradouro</h2>
                    <p>Retorna uma lista de enderecos correspondentes aos filtros de UF, Cidade e Logradouro.</p>
                </div>

                <div class="quick-chips">
                    <span>Exemplos:</span>
                    <span class="chip" onclick="setLogradouro('RS', 'Porto Alegre', 'Domingos')">RS / Porto Alegre / Domingos</span>
                    <span class="chip" onclick="setLogradouro('SP', 'São Paulo', 'Paulista')">SP / Sao Paulo / Paulista</span>
                </div>

                <form id="form-logradouro" onsubmit="handleLogradouro(event)">
                    <div class="form-row">
                        <div class="form-group" style="max-width: 90px;">
                            <label for="uf-input">UF:</label>
                            <input type="text" id="uf-input" placeholder="SP" maxlength="2" required>
                        </div>
                        <div class="form-group">
                            <label for="cidade-input">Cidade:</label>
                            <input type="text" id="cidade-input" placeholder="Sao Paulo" required>
                        </div>
                        <div class="form-group">
                            <label for="rua-input">Logradouro / Rua (min. 3 caracteres):</label>
                            <input type="text" id="rua-input" placeholder="Paulista" required>
                        </div>
                    </div>
                    <button type="submit" class="btn">Pesquisar Enderecos SOAP</button>
                </form>

                <div id="logradouro-result" class="result-panel"></div>
            </div>
        </div>

        <!-- Tab 4: Testador Raw XML -->
        <div id="tab-raw" class="tab-content" style="display: none;">
            <div class="card">
                <div class="card-header">
                    <h2>Testador Raw de Envelope SOAP 1.1</h2>
                    <p>Envie envelopes SOAP XML puros diretamente para o endpoint /soap e inspecione a resposta bruta.</p>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="raw-template">Template SOAP:</label>
                        <select id="raw-template" onchange="loadRawTemplate()">
                            <option value="consultar_cep">consultar_cep (01001-000)</option>
                            <option value="validar_cep">validar_cep (01001000)</option>
                            <option value="buscar_por_logradouro">buscar_por_logradouro (RS / Porto Alegre / Domingos)</option>
                            <option value="obter_status_servico">obter_status_servico</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="raw-action">SOAPAction Header:</label>
                        <input type="text" id="raw-action" value="consultar_cep">
                    </div>
                </div>

                <div class="form-group" style="margin-bottom: 1rem;">
                    <label for="raw-xml">Envelope XML SOAP 1.1:</label>
                    <textarea id="raw-xml" rows="9"></textarea>
                </div>

                <button type="button" class="btn" onclick="handleRawSoap()">Enviar Envelope SOAP POST</button>

                <div id="raw-result" class="result-panel"></div>
            </div>
        </div>

        <footer>
            Endpoint SOAP: /soap • Contrato: /soap?wsdl
        </footer>
    </div>

    <script>
        function switchTab(tabId, event) {
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            
            const targetContent = document.getElementById('tab-' + tabId);
            if (targetContent) targetContent.style.display = 'block';
            
            if (event && event.currentTarget) {
                event.currentTarget.classList.add('active');
            }
        }

        function setConsultarCep(cep) {
            document.getElementById('cep-input').value = cep;
        }

        function setLogradouro(uf, cidade, rua) {
            document.getElementById('uf-input').value = uf;
            document.getElementById('cidade-input').value = cidade;
            document.getElementById('rua-input').value = rua;
        }

        async function callSoap(action, bodyXml) {
            const envelope = `<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
    <soapenv:Header/>
    <soapenv:Body>
        ${bodyXml}
    </soapenv:Body>
</soapenv:Envelope>`;

            const startTime = performance.now();
            const response = await fetch('/soap', {
                method: 'POST',
                headers: {
                    'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': action
                },
                body: envelope
            });

            const durationMs = Math.round(performance.now() - startTime);
            const responseText = await response.text();
            
            return {
                status: response.status,
                durationMs: durationMs,
                requestXml: envelope,
                responseXml: responseText
            };
        }

        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        }

        function extractXmlTag(xmlString, tag) {
            const regex = new RegExp(`<.*?${tag}>(.*?)</.*?${tag}>`, 's');
            const match = xmlString.match(regex);
            return match ? match[1].trim() : '';
        }

        async function handleConsultar(e) {
            e.preventDefault();
            const cep = document.getElementById('cep-input').value.trim();
            const resultDiv = document.getElementById('consultar-result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<p style="color: var(--text-muted); font-size: 0.8125rem;">Enviando requisicao SOAP...</p>';

            try {
                const rpcBody = `<spy:consultar_cep><spy:cep>${escapeHtml(cep)}</spy:cep></spy:consultar_cep>`;
                const res = await callSoap('consultar_cep', rpcBody);

                const sucesso = extractXmlTag(res.responseXml, 'sucesso') === 'true';
                const mensagem = extractXmlTag(res.responseXml, 'mensagem') || 'Sem mensagem';
                
                let html = '';
                if (sucesso) {
                    const fields = {
                        'CEP': extractXmlTag(res.responseXml, 'cep'),
                        'Logradouro': extractXmlTag(res.responseXml, 'logradouro'),
                        'Complemento': extractXmlTag(res.responseXml, 'complemento') || 'Nenhum',
                        'Bairro': extractXmlTag(res.responseXml, 'bairro'),
                        'Cidade': extractXmlTag(res.responseXml, 'localidade'),
                        'Estado (UF)': extractXmlTag(res.responseXml, 'uf'),
                        'Codigo IBGE': extractXmlTag(res.responseXml, 'ibge'),
                        'DDD': extractXmlTag(res.responseXml, 'ddd')
                    };

                    html += `<div class="status-box success">[OK] ${escapeHtml(mensagem)} (${res.durationMs}ms)</div>`;
                    html += `<div class="result-grid">`;
                    for (const [key, val] of Object.entries(fields)) {
                        html += `
                            <div class="result-item">
                                <div class="label">${key}</div>
                                <div class="val">${escapeHtml(val) || '-'}</div>
                            </div>
                        `;
                    }
                    html += `</div>`;
                } else {
                    html += `<div class="status-box error">[ERRO] ${escapeHtml(mensagem)} (${res.durationMs}ms)</div>`;
                }

                html += `
                    <details class="xml-box" open>
                        <summary>Envelopes SOAP (Request / Response)</summary>
                        <div class="xml-title">SOAP Request (POST /soap):</div>
                        <pre class="xml-content">${escapeHtml(res.requestXml)}</pre>
                        <div class="xml-title" style="border-top: 1px solid var(--border-subtle);">SOAP Response (HTTP ${res.status}):</div>
                        <pre class="xml-content">${escapeHtml(res.responseXml)}</pre>
                    </details>
                `;

                resultDiv.innerHTML = html;
            } catch (err) {
                resultDiv.innerHTML = `<div class="status-box error">[ERRO] Falha de comunicacao: ${escapeHtml(err.message)}</div>`;
            }
        }

        async function handleValidar(e) {
            e.preventDefault();
            const cep = document.getElementById('cep-val-input').value.trim();
            const resultDiv = document.getElementById('validar-result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<p style="color: var(--text-muted); font-size: 0.8125rem;">Validando via SOAP...</p>';

            try {
                const rpcBody = `<spy:validar_cep><spy:cep>${escapeHtml(cep)}</spy:cep></spy:validar_cep>`;
                const res = await callSoap('validar_cep', rpcBody);

                const valido = extractXmlTag(res.responseXml, 'valido') === 'true';
                const mensagem = extractXmlTag(res.responseXml, 'mensagem');
                const cepFormatado = extractXmlTag(res.responseXml, 'cep_formatado');

                let html = '';
                if (valido) {
                    html += `<div class="status-box success">[OK] ${escapeHtml(mensagem)} (Formatado: ${escapeHtml(cepFormatado)})</div>`;
                } else {
                    html += `<div class="status-box error">[ERRO] ${escapeHtml(mensagem)}</div>`;
                }

                html += `
                    <details class="xml-box" open>
                        <summary>Envelopes SOAP (Request / Response)</summary>
                        <div class="xml-title">SOAP Request:</div>
                        <pre class="xml-content">${escapeHtml(res.requestXml)}</pre>
                        <div class="xml-title" style="border-top: 1px solid var(--border-subtle);">SOAP Response:</div>
                        <pre class="xml-content">${escapeHtml(res.responseXml)}</pre>
                    </details>
                `;

                resultDiv.innerHTML = html;
            } catch (err) {
                resultDiv.innerHTML = `<div class="status-box error">[ERRO] Falha de comunicacao: ${escapeHtml(err.message)}</div>`;
            }
        }

        async function handleLogradouro(e) {
            e.preventDefault();
            const uf = document.getElementById('uf-input').value.trim();
            const cidade = document.getElementById('cidade-input').value.trim();
            const rua = document.getElementById('rua-input').value.trim();
            const resultDiv = document.getElementById('logradouro-result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<p style="color: var(--text-muted); font-size: 0.8125rem;">Consultando logradouro via SOAP...</p>';

            try {
                const rpcBody = `<spy:buscar_por_logradouro><spy:uf>${escapeHtml(uf)}</spy:uf><spy:cidade>${escapeHtml(cidade)}</spy:cidade><spy:logradouro>${escapeHtml(rua)}</spy:logradouro></spy:buscar_por_logradouro>`;
                const res = await callSoap('buscar_por_logradouro', rpcBody);

                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(res.responseXml, 'text/xml');
                const items = xmlDoc.getElementsByTagNameNS('*', 'EnderecoResponse');

                let html = '';
                if (items.length > 0) {
                    html += `<div class="status-box success">[OK] ${items.length} endereco(s) localizado(s) (${res.durationMs}ms)</div>`;
                    html += `<div class="table-responsive"><table><thead><tr><th>CEP</th><th>Logradouro</th><th>Bairro</th><th>Cidade / UF</th><th>IBGE</th><th>DDD</th></tr></thead><tbody>`;
                    
                    for (let i = 0; i < items.length; i++) {
                        const it = items[i];
                        const g = tag => {
                            const node = it.getElementsByTagNameNS('*', tag)[0];
                            return node ? node.textContent : '';
                        };
                        html += `<tr>
                            <td><strong style="color: #fff; font-family: var(--mono);">${escapeHtml(g('cep'))}</strong></td>
                            <td>${escapeHtml(g('logradouro'))}</td>
                            <td>${escapeHtml(g('bairro'))}</td>
                            <td>${escapeHtml(g('localidade'))} / ${escapeHtml(g('uf'))}</td>
                            <td>${escapeHtml(g('ibge'))}</td>
                            <td>${escapeHtml(g('ddd'))}</td>
                        </tr>`;
                    }
                    html += `</tbody></table></div>`;
                } else {
                    html += `<div class="status-box error">[ERRO] Nenhum endereco localizado para os criterios informados.</div>`;
                }

                html += `
                    <details class="xml-box">
                        <summary>Envelopes SOAP (Request / Response)</summary>
                        <div class="xml-title">SOAP Request:</div>
                        <pre class="xml-content">${escapeHtml(res.requestXml)}</pre>
                        <div class="xml-title" style="border-top: 1px solid var(--border-subtle);">SOAP Response:</div>
                        <pre class="xml-content">${escapeHtml(res.responseXml)}</pre>
                    </details>
                `;

                resultDiv.innerHTML = html;
            } catch (err) {
                resultDiv.innerHTML = `<div class="status-box error">[ERRO] Falha de comunicacao: ${escapeHtml(err.message)}</div>`;
            }
        }

        const rawTemplates = {
            consultar_cep: {
                action: 'consultar_cep',
                xml: `<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:consultar_cep>
         <spy:cep>01001-000</spy:cep>
      </spy:consultar_cep>
   </soapenv:Body>
</soapenv:Envelope>`
            },
            validar_cep: {
                action: 'validar_cep',
                xml: `<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:validar_cep>
         <spy:cep>01001000</spy:cep>
      </spy:validar_cep>
   </soapenv:Body>
</soapenv:Envelope>`
            },
            buscar_por_logradouro: {
                action: 'buscar_por_logradouro',
                xml: `<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:buscar_por_logradouro>
         <spy:uf>RS</spy:uf>
         <spy:cidade>Porto Alegre</spy:cidade>
         <spy:logradouro>Domingos</spy:logradouro>
      </spy:buscar_por_logradouro>
   </soapenv:Body>
</soapenv:Envelope>`
            },
            obter_status_servico: {
                action: 'obter_status_servico',
                xml: `<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="api.soap.cep">
   <soapenv:Header/>
   <soapenv:Body>
      <spy:obter_status_servico/>
   </soapenv:Body>
</soapenv:Envelope>`
            }
        };

        function loadRawTemplate() {
            const key = document.getElementById('raw-template').value;
            const tpl = rawTemplates[key];
            if (tpl) {
                document.getElementById('raw-action').value = tpl.action;
                document.getElementById('raw-xml').value = tpl.xml;
            }
        }

        async function handleRawSoap() {
            const action = document.getElementById('raw-action').value.trim();
            const xmlBody = document.getElementById('raw-xml').value;
            const resultDiv = document.getElementById('raw-result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<p style="color: var(--text-muted); font-size: 0.8125rem;">Enviando envelope SOAP HTTP POST...</p>';

            try {
                const startTime = performance.now();
                const response = await fetch('/soap', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': action
                    },
                    body: xmlBody
                });
                const durationMs = Math.round(performance.now() - startTime);
                const responseText = await response.text();

                resultDiv.innerHTML = `
                    <div class="status-box ${response.ok ? 'success' : 'error'}">
                        HTTP Status: ${response.status} ${response.statusText || ''} | Tempo: ${durationMs}ms
                    </div>
                    <details class="xml-box" open>
                        <summary>Resposta SOAP XML Bruta do Servidor</summary>
                        <pre class="xml-content">${escapeHtml(responseText)}</pre>
                    </details>
                `;
            } catch (err) {
                resultDiv.innerHTML = `<div class="status-box error">[ERRO] Falha ao executar chamada SOAP Raw: ${escapeHtml(err.message)}</div>`;
            }
        }

        loadRawTemplate();
    </script>
</body>
</html>
"""

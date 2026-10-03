"""Record a demo video for one portfolio project.

Usage (from the repository root): python .github/demo/record.py <name> <out_dir>
Web apps are driven with Playwright, command line tools are captured from a real
terminal session and replayed in a terminal-style page, and the game is recorded
straight from its render loop. Every video ends up as <out_dir>/<name>-demo.mp4 + .gif.
"""
import asyncio, json, math, os, random, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from webrec import record, step, wait_for_http, encode  # noqa: E402

NAME, OUT = sys.argv[1], os.path.abspath(sys.argv[2])
os.makedirs(OUT, exist_ok=True)
BASE = os.path.join(OUT, NAME + '-demo')
GH = 'github.com/Matthew-Uhlar'


def sh(cmd, cwd=ROOT, env=None):
    o = subprocess.run(['bash', '-c', cmd], cwd=cwd, capture_output=True, text=True, env=env)
    return o.stdout + o.stderr


def bg(cmd, cwd=ROOT, env=None):
    return subprocess.Popen(['bash', '-c', cmd], cwd=cwd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def term(spec):
    path = BASE + '.json'
    json.dump(spec, open(path, 'w'))
    subprocess.run([sys.executable, os.path.join(HERE, 'termdemo.py'), path, BASE], check=True)
    os.remove(path)


def link(p, name):
    return p.get_by_role('link', name=name, exact=True).first


# ---------------------------------------------------------------- Docker web apps
async def ai_pm(p, r):
    U = 'http://localhost:5173'
    await p.goto(U + '/login'); await p.wait_for_timeout(1200)
    await r.cap('Project Pilot: AI-assisted Agile planning tool  |  ASP.NET Core 8, EF Core, PostgreSQL, React + TypeScript', 2600)
    async def login():
        await r.cap('JWT sign-in with role-based access (admin and team member)', 600)
        await r.click(p.get_by_role('button', name='Sign in'), 2200)
    await step(p, 'login', login())
    async def dash():
        await r.cap('Dashboard: sprint progress, story points and workload at a glance', 1800)
        await r.scroll(450); await p.wait_for_timeout(1500); await r.scroll(-450); await p.wait_for_timeout(500)
    await step(p, 'dashboard', dash())
    async def board():
        await r.click(link(p, 'Sprint Board'), 1500)
        await r.cap('Kanban sprint board with drag and drop (status saved through the REST API)', 1200)
        card = p.locator('.work-card').first
        await r.point(card, click=False)
        await card.drag_to(p.locator('.board-column').nth(1)); await p.wait_for_timeout(1800)
    await step(p, 'board', board())
    async def backlog():
        await r.click(link(p, 'Backlog'), 1300)
        await r.cap('Backlog: add work items with priority and story points', 500)
        f = p.locator('form').first
        await r.type(f.locator('input').first, 'Parent check-in kiosk', 40)
        await r.type(f.locator('textarea').first, 'Let parents check children in and out from a tablet at the front desk.', 18)
        await f.locator('select').nth(0).select_option('High'); await p.wait_for_timeout(400)
        await f.locator('select').nth(1).select_option('5'); await p.wait_for_timeout(400)
        await r.click(p.get_by_role('button', name='Add to backlog'), 1800)
    await step(p, 'backlog', backlog())
    async def assistant():
        await r.click(link(p, 'AI Assistant'), 1300)
        await r.cap('AI assistant: turn a plain-language idea into user stories with suggested points', 500)
        await r.type(p.locator('textarea').first, 'Let staff scan a QR code to update classroom inventory from a phone', 30)
        await r.click(p.get_by_role('button', name='Generate stories'), 300)
        await p.locator('.generated-section').wait_for(timeout=15000)
        await p.locator('.generated-section').scroll_into_view_if_needed(); await p.wait_for_timeout(1500)
        await r.scroll(500); await p.wait_for_timeout(1800)
    await step(p, 'assistant', assistant())
    async def risk():
        await p.evaluate('window.scrollTo({top:0,behavior:"smooth"})'); await p.wait_for_timeout(800)
        await r.cap('Risk review flags oversized stories and missing owners; sprint summary drafts a status update', 300)
        await r.click(p.get_by_role('button', name='Run risk review'), 2200)
        await r.click(p.get_by_role('button', name='Create sprint summary'), 2500)
        await r.scroll(350); await p.wait_for_timeout(1500)
    await step(p, 'risk', risk())
    await r.cap('The AI layer sits behind an IAiPlanningService interface, so a hosted LLM provider can be swapped in', 3000)
    await r.cap('Project Pilot  |  C#, ASP.NET Core 8, EF Core, PostgreSQL, React, TypeScript, Docker  |  ' + GH, 3000)


async def emergency(p, r):
    U = 'http://localhost:5174'
    await p.goto(U + '/login'); await p.wait_for_timeout(1200)
    await r.cap('Response Grid: real-time emergency dispatch platform  |  ASP.NET Core 8, SignalR, PostgreSQL, React', 2600)
    async def login():
        await r.cap('Dispatcher and responder roles with JWT authentication', 500)
        await r.click(p.get_by_role('button', name='Sign in'), 2200)
    await step(p, 'login', login())
    async def dash():
        await r.cap('Live dashboard: open incidents, unit availability and recent activity', 2000)
        await r.scroll(450); await p.wait_for_timeout(1500); await r.scroll(-450)
    await step(p, 'dashboard', dash())
    async def create():
        await r.click(link(p, 'Incidents'), 1300)
        await r.cap('Dispatchers create incidents with severity and coordinates for mapping', 500)
        f = p.locator('form').first
        ins = f.locator('input')
        await r.type(ins.nth(0), 'Traffic signal outage at intersection', 30)
        await r.type(f.locator('textarea').first, 'All signals dark at Congress Ave and Cesar Chavez during rush hour.', 15)
        await r.type(ins.nth(1), '100 Congress Ave, Austin, TX', 25)
        await ins.nth(2).fill('30.2622'); await ins.nth(3).fill('-97.7452'); await p.wait_for_timeout(400)
        await f.locator('select').select_option('High'); await p.wait_for_timeout(500)
        await r.click(p.get_by_role('button', name='Create incident'), 2000)
    await step(p, 'create', create())
    async def detail():
        await r.click(p.locator('.incident-card', has_text='Traffic signal outage').first, 1800)
        await r.cap('Assign an available unit; every action lands in the incident timeline', 500)
        await p.locator('select').first.select_option(index=1); await p.wait_for_timeout(600)
        await r.click(p.get_by_role('button', name='Assign'), 1800)
        await r.cap('Status updates broadcast to every connected client through SignalR', 500)
        await p.locator('select').nth(1).select_option('Dispatched'); await p.wait_for_timeout(400)
        await r.type(p.locator('textarea').first, 'Utility 4 en route. APD requested for traffic control.', 18)
        await r.click(p.get_by_role('button', name='Save update'), 2000)
        await r.scroll(500); await p.wait_for_timeout(2000)
    await step(p, 'detail', detail())
    async def units():
        await r.click(link(p, 'Response Units'), 1500)
        await r.cap('Response units and their live status', 2500)
    await step(p, 'units', units())
    await r.cap('Response Grid  |  C#, ASP.NET Core 8, SignalR, EF Core, PostgreSQL, React, TypeScript, Docker  |  ' + GH, 3000)


async def inventory(p, r):
    U = 'http://localhost:5173'
    await p.goto(U + '/login'); await p.wait_for_timeout(1200)
    await r.cap('StockPilot: enterprise inventory and asset management  |  ASP.NET Core 8, PostgreSQL, React + TypeScript', 2600)
    await step(p, 'login', r.click(p.get_by_role('button', name='Sign in'), 2200))
    await r.cap('Dashboard: inventory value, low-stock items, assets and pending purchase requests', 2500)
    async def inv():
        await r.click(link(p, 'Inventory'), 1500)
        await r.cap('Inventory with reorder levels (low rows are highlighted) and live search', 1500)
        await r.type(p.get_by_placeholder('Search'), 'toner', 90); await p.wait_for_timeout(1500)
        await p.get_by_placeholder('Search').fill(''); await p.get_by_placeholder('Search').press('Backspace'); await p.wait_for_timeout(800)
        await r.cap('Admins add stock items (role-based authorization on the API)', 400)
        for ph, val in [('sku', 'NET-SW-024'), ('name', '24-port network switch'), ('category', 'Networking'), ('location', 'IT closet B')]:
            await r.type(p.get_by_placeholder(ph, exact=True), val, 20)
        for ph, val in [('quantity', '2'), ('reorderLevel', '3'), ('unitCost', '189.99')]:
            await p.get_by_placeholder(ph, exact=True).fill(val); await p.wait_for_timeout(250)
        await r.click(p.get_by_role('button', name='Add item'), 1800)
        await r.scroll(500); await p.wait_for_timeout(1500)
    await step(p, 'inventory', inv())
    async def assets():
        await r.click(link(p, 'Assets'), 1500)
        await r.cap('Asset tracking: who has which laptop, where and in what condition', 2500)
    await step(p, 'assets', assets())
    async def reqs():
        await r.click(link(p, 'Requests'), 1300)
        await r.cap('Purchase request workflow: submit, then approve or reject as an admin', 400)
        await r.type(p.get_by_placeholder('Item name'), 'Laptop docking stations', 25)
        await p.locator('input[type=number]').first.fill('6'); await p.wait_for_timeout(300)
        await r.type(p.get_by_placeholder('Business reason'), 'New hires starting next month', 20)
        await r.click(p.get_by_role('button', name='Submit request'), 1800)
        await r.click(p.get_by_role('button', name='Approve').last, 2200)
    await step(p, 'requests', reqs())
    await r.cap('StockPilot  |  C#, ASP.NET Core 8, EF Core, PostgreSQL, React, TypeScript, Docker  |  ' + GH, 3000)


async def supportflow():
    API = 'http://localhost:8090'
    env_file = '/tmp/sf.env'
    open(env_file, 'w').write('')
    steps = []
    def run(cmd, note=None, show=True, **k):
        out = sh(f'source {env_file}; {cmd}')
        print('$', cmd, '\n', out[:500], flush=True)
        if show:
            steps.append(dict(cmd=cmd, out=out, note=note, cwd='~/supportflow', **k))
    H = '-H "Content-Type: application/json"'
    def login(var, email, pw, note=None, show=True):
        body = '{"email":"%s","password":"%s"}' % (email, pw)
        run(f"""echo "export {var}=$(curl -s -X POST {API}/api/auth/login {H} -d '{body}' | jq -r .token)" >> {env_file}""", show=False)
        if show:
            run(f"""curl -s -X POST {API}/api/auth/login {H} -d '{body}' | jq '{{name, role, token: (.token[0:32] + "...")}}'""", note, pause=2600)
    await wait_for_http(API + '/swagger-ui.html', 300)
    login('EMP', 'employee@example.com', 'Employee123!', 'SupportFlow: help desk API in Java 21 + Spring Boot 3. Sign in as an employee (JWT)')
    run(f"""curl -s -X POST {API}/api/tickets {H} -H "Authorization: Bearer $EMP" -d '{{"title":"Outlook keeps asking for my password","description":"Started after the Windows update this morning.","priority":"HIGH"}}' | jq '{{id, title, priority, status, createdBy: .createdBy.name}}'""", 'Employees submit tickets (validated with Bean Validation)', pause=2800, clear=True)
    tid = sh(f"source {env_file}; curl -s {API}/api/tickets -H \"Authorization: Bearer $EMP\" | jq '[.[].id] | max'").strip() or '3'
    run(f"""curl -s -o /dev/null -w "HTTP %{{http_code}}\\n" -X PATCH {API}/api/tickets/{tid} {H} -H "Authorization: Bearer $EMP" -d '{{"status":"RESOLVED"}}'""", 'Spring Security method rules: employees cannot change ticket status', pause=2600)
    login('TECH', 'tech@example.com', 'Tech123!', 'Sign in as a technician')
    run(f"""curl -s -X PATCH {API}/api/tickets/{tid} {H} -H "Authorization: Bearer $TECH" -d '{{"status":"IN_PROGRESS","priority":"CRITICAL"}}' | jq '{{id, status, priority, history: [.history[].changeDescription]}}'""", 'Technicians move tickets through the workflow; every change is written to the audit history', pause=3200, clear=True)
    run(f"""curl -s -X POST {API}/api/tickets/{tid}/comments {H} -H "Authorization: Bearer $TECH" -d '{{"message":"Cleared cached credentials, asking user to retry.","internal":false}}' | jq '{{message, internal, author: .author.name}}'""", 'Comments and internal notes', pause=2600)
    login('ADMIN', 'admin@example.com', 'Admin123!', show=False)
    run(f"""curl -s "{API}/api/tickets?status=IN_PROGRESS" -H "Authorization: Bearer $ADMIN" | jq '[.[] | {{id, title, status, priority}}]'""", 'Filter tickets by status or priority', pause=2800, clear=True)
    run(f"""curl -s {API}/api/dashboard -H "Authorization: Bearer $ADMIN" | jq .""", 'Dashboard reporting endpoint for administrators', pause=3000)
    spec = dict(title='SupportFlow API  |  Java 21, Spring Boot 3, Spring Security, PostgreSQL', caption='SupportFlow',
                final='Next: the same API documented with OpenAPI / Swagger UI', steps=steps)
    global BASE
    final_base = BASE
    BASE = final_base + '-term'; term(spec)
    async def swagger(p, r):
        await p.goto(API + '/swagger-ui.html'); await p.wait_for_timeout(2500)
        await r.cap('OpenAPI documentation generated with springdoc: every endpoint, schema and auth requirement', 2500)
        await r.scroll(500); await p.wait_for_timeout(1500)
        await step(p, 'swagger expand', r.click(p.locator('.opblock-summary').first, 2500))
        await r.cap('SupportFlow  |  Java 21, Spring Boot 3, Spring Security, JPA, PostgreSQL, JUnit 5, Docker  |  ' + GH, 3000)
    await record(final_base + '-swagger', swagger)
    with open('/tmp/concat.txt', 'w') as f:
        f.write(f"file '{final_base}-term.mp4'\nfile '{final_base}-swagger.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', '/tmp/concat.txt', '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-crf', '26', '-movflags', '+faststart', final_base + '.mp4'], check=True)
    os.replace(final_base + '-term.gif', final_base + '.gif')
    for ext in ('-term.mp4', '-swagger.mp4', '-swagger.gif'):
        if os.path.exists(final_base + ext):
            os.remove(final_base + ext)


# ---------------------------------------------------------------- local web apps
async def childcare(p, r):
    U = 'http://localhost:5055'
    await p.goto(U + '/login'); await r.cap('Childcare Inventory System: Flask + SQLite app for a childcare center', 2200)
    await r.cap('Role-based login (admin, manager, staff) with hashed passwords', 800)
    await r.click(p.locator('button[type=submit]'), 1500)
    await r.cap('Dashboard: total items, low-stock alerts and pending supply requests', 2500)
    await r.scroll(300); await p.wait_for_timeout(1200)
    await r.click(link(p, 'Inventory'), 1200)
    await r.cap('Inventory list with search by item or category', 1500)
    await r.type(p.locator('input[name=search]'), 'diaper'); await r.click(p.locator('button[type=submit]').first, 1800)
    await r.cap('Adding a new supply item with validation', 600)
    await p.goto(U + '/inventory'); await p.wait_for_timeout(500)
    await r.click(p.locator('a.button', has_text='Add').first, 1000)
    await r.type(p.locator('input[name=name]'), 'Hand Sanitizer')
    await r.type(p.locator('input[name=category]'), 'Health')
    await r.type(p.locator('input[name=quantity]'), '2', 120)
    await r.type(p.locator('input[name=unit_type]'), 'bottles')
    await r.type(p.locator('input[name=minimum_stock]'), '6', 120)
    await r.click(p.locator('button[type=submit]'), 1800)
    await r.cap('Below its minimum, so it is flagged as low stock', 2200)
    await r.click(p.get_by_role('link', name='Requests').first, 1200)
    await r.cap('Staff submit supply requests for manager approval', 800)
    await p.locator('select[name=item_id]').select_option(index=1); await p.wait_for_timeout(600)
    await r.type(p.locator('input[name=requested_quantity]'), '12', 120)
    await r.type(p.locator('textarea[name=notes]'), 'Restock for the toddler rooms', 35)
    await r.click(p.locator('button[type=submit]'), 1800)
    await r.cap('Managers approve, deny or complete each request', 900)
    await r.click(p.locator('a.button', has_text='Approve').first, 2200)
    await r.click(p.get_by_role('link', name='Dashboard').first, 1500)
    await r.cap('Childcare Inventory System  |  Python, Flask, SQLite, Jinja  |  ' + GH, 3000)


async def tracker(p, r):
    U = 'http://127.0.0.1:3000/'
    jobs = [('Four Hands', 'Software Engineer - New Grad', 'Applied', 'https://example.com/jobs/1', 'Hybrid in Austin. Followed up with recruiter on LinkedIn.'),
            ('Tank Payments', 'Software Engineer', 'Interview', 'https://example.com/jobs/2', 'Phone screen Tuesday. Review Spring Boot and SQL joins.'),
            ('Nexus Real Estate', 'Backend Engineer', 'Saved', 'https://example.com/jobs/3', 'C# and PostgreSQL stack. Tailor resume before applying.')]
    await p.goto(U); await r.cap('Application Tracker: TypeScript job-search pipeline with zero runtime dependencies', 2200)
    for i, (c, ro, st, u, n) in enumerate(jobs):
        if i == 0: await r.cap('Create an application: company, role, status, posting URL and notes', 300)
        await r.click(p.locator('#new'), 700)
        await r.type(p.locator('#company'), c, 40 if i == 0 else 15)
        await r.type(p.locator('#role'), ro, 35 if i == 0 else 12)
        await r.point(p.locator('#status')); await p.locator('#status').select_option(st); await p.wait_for_timeout(400)
        await r.type(p.locator('#url'), u, 20 if i == 0 else 8)
        await r.type(p.locator('#notes'), n, 25 if i == 0 else 8)
        await r.click(p.locator('#form button[type=submit]'), 900)
        if i == 0: await r.cap('Runtime validation shares the same typed module on server and browser', 300)
    await r.cap('Status totals update across the whole collection', 1500)
    await r.scroll(420); await p.wait_for_timeout(1500)
    await r.cap('Search company, role and notes', 300)
    await r.type(p.locator('#search'), 'spring', 90); await p.wait_for_timeout(1800)
    await p.locator('#search').fill(''); await p.wait_for_timeout(600)
    await r.cap('Filter by pipeline stage', 300)
    await r.point(p.locator('#filter')); await p.locator('#filter').select_option('Interview'); await p.wait_for_timeout(1800)
    await p.locator('#filter').select_option(index=0); await p.wait_for_timeout(800)
    await r.cap('Edit an application as it moves through the pipeline (moving backward is allowed too)', 300)
    await r.click(p.get_by_role('button', name='Edit Backend Engineer at Nexus Real Estate'), 900)
    await p.locator('#status').select_option('Applied'); await p.wait_for_timeout(700)
    await r.click(p.locator('#form button[type=submit]'), 1500)
    await r.cap('Data persists in browser storage and can be exported / imported as validated JSON backups', 2500)
    await p.reload(); await p.wait_for_timeout(1500)
    await r.cap('Application Tracker  |  TypeScript, Node.js, HTML, CSS, node:test  |  ' + GH, 3000)


async def prestige(p, r):
    U = 'http://localhost:8077/'
    await p.goto(U + 'index.html'); await p.wait_for_timeout(1500)
    await r.cap('Prestige Construction: responsive marketing site built for a Colorado general contractor', 3000)
    await r.cap('Responsive HTML5/CSS3 layout with a video hero, service sections and project gallery', 300)
    for _ in range(6): await r.scroll(520, 6, 180); await p.wait_for_timeout(900)
    await r.cap('Portfolio page showcasing completed projects', 300)
    await p.goto(U + 'generic.html'); await p.wait_for_timeout(1500)
    for _ in range(3): await r.scroll(500, 6, 180); await p.wait_for_timeout(800)
    await r.cap('Quote request form (PHP mail handler on the live server)', 300)
    await p.goto(U + 'quote.html'); await p.wait_for_timeout(1200)
    await p.locator('form').first.scroll_into_view_if_needed(); await p.wait_for_timeout(600)
    await r.type(p.locator('#vname'), 'Jordan Smith', 45)
    await r.type(p.locator('#vemail'), 'jordan@example.com', 30)
    await r.type(p.locator('#message'), 'Looking for a quote on a kitchen remodel and a new deck.', 25)
    await p.wait_for_timeout(1000)
    await p.goto(U + 'index.html'); await p.wait_for_timeout(800)
    await r.cap('Prestige Construction website  |  HTML5, CSS3, JavaScript, jQuery, PHP  |  ' + GH, 3000)


# ---------------------------------------------------------------- terminal demos
def sentinelhash():
    d = os.path.join(ROOT, 'projects/sentinelhash')
    sh('cargo build --release -q', cwd=d)
    sh(f'sudo cp target/release/sentinelhash /usr/local/bin/', cwd=d)
    w = '/tmp/shdemo'
    sh(f'rm -rf {w} && mkdir -p {w}/server/config {w}/server/www {w}/server/logs')
    sh("""echo '{"port":8080,"debug":false}' > server/config/settings.json; echo '<h1>Welcome</h1>' > server/www/index.html;
          echo 'body{}' > server/www/site.css; echo 'admin:x:1000' > server/config/users.conf;
          for i in 1 2 3 4 5; do echo "page $i" > server/www/page$i.html; done; echo log > server/logs/app.log""", cwd=w)
    steps = []
    def add(cmd, note=None, **k):
        steps.append(dict(cmd=cmd, out=sh(cmd, cwd=w), note=note, cwd='~/demo', **k))
    add('find server -type f | sort', 'A sample web server directory we want to protect', pause=2200)
    add('sentinelhash baseline ./server --output baseline.json --ignore "*.log"', 'Step 1: record a trusted SHA-256 baseline (files hashed in parallel with Rayon)')
    add("""sed -i 's/false/true/' server/config/settings.json && echo 'eviluser:x:0' >> server/config/users.conf""", 'Step 2: simulate an attacker changing config files...', pause=1200)
    add("""echo '<?php system($_GET["c"]); ?>' > server/www/shell.php && rm server/www/page3.html""", '...dropping a web shell and deleting a page', pause=1200, clear=True)
    add('sentinelhash check ./server --baseline baseline.json --ignore "*.log" --report report.json', 'Step 3: compare against the baseline. Every change is caught', pause=4500)
    add("""python3 -c "import json;r=json.load(open('report.json'));print(json.dumps(r['added'],indent=2))\"""", 'Step 4: a machine-readable JSON report for SIEM / audit tooling', pause=3500)
    term(dict(title='SentinelHash  |  Rust file integrity monitor', caption='SentinelHash: detect added, modified and deleted files with SHA-256',
              final='SentinelHash  |  Rust, Rayon, Serde, Clap  |  ' + GH, steps=steps))


def ticket_api():
    d = os.path.join(ROOT, 'showcase/support-ticket-api')
    sh('rm -f /tmp/t.db && python3 server.py --db /tmp/t.db --seed', cwd=d)
    srv = bg('python3 server.py --db /tmp/t.db --port 8000', cwd=d); time.sleep(2)
    steps = []
    def add(cmd, note=None, **k):
        steps.append(dict(cmd=cmd, out=sh(cmd, cwd=d), note=note, cwd='~/support-ticket-api', **k))
    J = ' | python3 -m json.tool'; H = ' -H "Content-Type: application/json"'
    add('python3 -m unittest discover 2>&1 | tail -3', 'Integration tests spin up a real HTTP server on a temp SQLite database', pause=2000)
    add('curl -s "localhost:8000/tickets?limit=2"' + J, 'List tickets newest first, with paging, status filter and search', fast=True, pause=2500, clear=True)
    add("curl -s -X POST localhost:8000/tickets" + H + """ -d '{"title":"VPN drops every hour","description":"Remote staff lose the VPN tunnel hourly."}'""" + J, 'Create a ticket (validated JSON, 201 Created)', pause=2500)
    add("curl -s -X PATCH localhost:8000/tickets/4" + H + """ -d '{"status":"in_progress"}'""" + J, 'Move it through the status workflow', fast=True, pause=2200, clear=True)
    add("curl -s -i -X PATCH localhost:8000/tickets/4" + H + """ -d '{"status":"closed"}' | sed -n '1p;$p'""", 'Invalid transitions are rejected with 409 Conflict and nothing changes', pause=3000)
    add("curl -s -X POST localhost:8000/tickets/4/comments" + H + """ -d '{"body":"Replaced router firmware, monitoring."}'""" + J, 'Add comments to a ticket', pause=2000, clear=True)
    add('curl -s localhost:8000/reports' + J, 'Reporting endpoint: totals per status', pause=3200)
    srv.terminate()
    term(dict(title='Support Ticket API  |  Python standard library + SQLite', caption='Support Ticket API',
              final='Support Ticket API  |  Python, SQLite, SQL transactions, unittest  |  ' + GH, steps=steps))


def dependency_lens():
    d = os.path.join(ROOT, 'showcase/dependency-lens')
    files = {
        'src/main.ts': "import { renderApp } from './ui/app'\nimport { loadConfig } from './config'\nrenderApp(loadConfig())\n",
        'src/config.ts': 'export const loadConfig = () => ({})\n',
        'src/ui/app.tsx': "import React from 'react'\nimport { Cart } from '../cart/cart'\nimport { fetchProducts } from '../api/client'\nexport function renderApp(c) { return [Cart, fetchProducts, c] }\n",
        'src/cart/cart.ts': "import { priceWithTax } from './pricing'\nimport { formatMoney } from '../ui/format'\nexport const Cart = { priceWithTax, formatMoney }\n",
        'src/cart/pricing.ts': "import { Cart } from './cart'\nexport const priceWithTax = (p) => p * 1.0825\n",
        'src/ui/format.ts': "export const formatMoney = (n) => '$' + n.toFixed(2)\n",
        'src/api/client.ts': "import axios from 'axios'\nimport { retry } from './retry'\nexport const fetchProducts = () => retry(() => axios.get('/products'))\n",
    }
    for rel, txt in files.items():
        path = os.path.join(d, 'my-shop', rel); os.makedirs(os.path.dirname(path), exist_ok=True); open(path, 'w').write(txt)
    steps = []
    def add(cmd, note=None, **k):
        steps.append(dict(cmd=cmd, out=sh(cmd, cwd=d), note=note, cwd='~/dependency-lens', **k))
    add('node --test 2>&1 | grep -E "^# (tests|pass|fail)"', 'Dependency Lens: a zero-dependency Node.js CLI that maps JS/TS imports', pause=1800)
    add('find my-shop -name "*.ts*" | sort', 'A small TypeScript app to analyze', pause=1800)
    add('node src/cli.js my-shop', 'Finds circular dependencies (Tarjan SCC) and unresolved relative imports', pause=3500)
    add('node src/cli.js my-shop --strict; echo "exit code: $?"', '--strict returns a non-zero exit code, so it can fail a CI build', pause=3000, clear=True)
    add('node src/cli.js my-shop --format mermaid', 'Export the graph as Mermaid (or JSON) for docs and code reviews', fast=True, pause=3500)
    sh('rm -rf my-shop', cwd=d)
    term(dict(title='Dependency Lens  |  Node.js CLI', caption='Dependency Lens',
              final='Dependency Lens  |  JavaScript, Node.js, graph algorithms, node:test  |  ' + GH, steps=steps))


def interactive(cmd, cwd, answers):
    import pexpect
    c = pexpect.spawn(cmd, cwd=cwd, encoding='utf-8', timeout=10, dimensions=(60, 120)); out = ''
    for prompt, ans in answers:
        c.expect(prompt); out += c.before + c.after; c.sendline(ans)
    c.expect(pexpect.EOF); out += c.before
    return out.replace('\r', '')


def csc500():
    d = '/tmp/CSC500/CSC500 Module 1'
    a = interactive('python3 arithmetic_program.py', d, [('first number: ', '84'), ('second number: ', '12')])
    b = interactive('python3 arithmetic_program.py', d, [('first number: ', '5'), ('second number: ', '0')])
    term(dict(title='CSC500 Module 1  |  Python', caption='CSC500', final='CSC500 Principles of Programming coursework  |  Python  |  ' + GH, steps=[
        dict(cmd='python3 arithmetic_program.py', out=a.strip(), note='Module 1: arithmetic calculator with input handling', pause=2500, cwd='~/CSC500'),
        dict(cmd='python3 arithmetic_program.py', out=b.strip(), note='Guards against division by zero', pause=3000, cwd='~/CSC500')]))


def csc500_cart():
    d = '/tmp/CSC500-Portfolio'
    t = interactive('python3 shopping_cart.py', d, [
        ('name: ', 'Matt Uhlar'), ('date: ', 'October 2, 2026'),
        ('option: ', 'a'), ('item name: ', 'Laptop Stand'), ('description: ', 'Aluminum adjustable stand'), ('price: ', '49.99'), ('quantity: ', '1'),
        ('option: ', 'a'), ('item name: ', 'USB-C Cable'), ('description: ', '6 ft braided cable'), ('price: ', '12.50'), ('quantity: ', '3'),
        ('option: ', 'c'), ('item name: ', 'USB-C Cable'), ('new quantity: ', '2'),
        ('option: ', 'o'), ('option: ', 'i'), ('option: ', 'q')])
    parts = t.split('Choose an option: ')
    notes = ['Add items to the cart', None, 'Change an item quantity', 'Output the cart with per-item and total cost', 'Output item descriptions', None]
    steps = [dict(cmd='python3 shopping_cart.py', out=parts[0] + 'Choose an option: ' + parts[1].split('\n')[0],
                  note='CSC500 final project: object-oriented shopping cart (ItemToPurchase + ShoppingCart classes)', pause=1500, cwd='~/CSC500-Portfolio')]
    for i in range(1, len(parts)):
        body = '\n'.join(parts[i].split('\n')[1:]).split('\nMENU')[0]
        nxt = parts[i + 1].split('\n')[0] if i + 1 < len(parts) else None
        out = body.strip('\n') + ('\n\nChoose an option: ' + nxt if nxt else '')
        if out.strip():
            steps.append(dict(cmd=None, out=out, note=notes[i - 1] if i - 1 < len(notes) else None, pause=2600, clear=True, cwd='~/CSC500-Portfolio'))
    term(dict(title='CSC500 Shopping Cart  |  Python OOP', caption='CSC500 Shopping Cart',
              final='CSC500 Online Shopping Cart  |  Python, classes and objects  |  ' + GH, steps=steps))


def signal_siege():
    os.environ['SDL_VIDEODRIVER'] = 'dummy'; os.environ['SDL_AUDIODRIVER'] = 'dummy'
    sys.path.insert(0, os.path.join(ROOT, 'projects/signal-siege')); os.chdir('/tmp')
    import pygame
    from game import core, settings
    random.seed(7)
    state = {'mouse': (600, 350), 'keys': set()}
    class Keys:
        def __getitem__(self, k): return k in state['keys']
    pygame.mouse.get_pos = lambda: state['mouse']
    pygame.mouse.get_pressed = lambda *a, **k: (True, False, False)
    pygame.key.get_pressed = lambda: Keys()
    g = core.Game(); W, H = settings.WIDTH, settings.HEIGHT
    font = pygame.font.SysFont('dejavusans', 22, bold=True)
    raw = BASE + '-raw.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H + 50}', '-r', '30', '-i', '-',
                           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', raw], stdin=subprocess.PIPE)
    caps = [(0, 'Signal Siege: wave-survival game in Python + Pygame (all graphics drawn in code)'), (9, 'Three enemy types with different behaviors chase the core'),
            (18, 'Between waves the player picks an upgrade'), (30, 'Particles, screen shake, shields and a progressive wave system'),
            (44, 'Signal Siege  |  Python, Pygame, OOP  |  ' + GH)]
    t = 0; dt = 1 / 30; wait = 0; frame = pygame.Surface((W, H + 50))
    while t < 52:
        pygame.event.pump(); p = g.player.position
        if g.enemies:
            e = min(g.enemies, key=lambda e: (e.position - p).length()); state['mouse'] = (int(e.position.x), int(e.position.y))
        ang = t * 0.9; tx = W / 2 + 170 * math.cos(ang); ty = H / 2 + 150 * math.sin(ang); keys = set()
        if tx > p.x + 8: keys.add(pygame.K_d)
        if tx < p.x - 8: keys.add(pygame.K_a)
        if ty > p.y + 8: keys.add(pygame.K_s)
        if ty < p.y - 8: keys.add(pygame.K_w)
        state['keys'] = keys
        if g.state == 'playing': g.update(dt)
        elif g.state == 'upgrade':
            wait += dt
            if wait > 2.2: g.select_upgrade(random.randint(0, 2)); wait = 0
        if g.player.health < 40: g.player.health = 100
        if g.core.health < 80: g.core.health = 200
        g.draw(); frame.fill((31, 111, 235)); frame.blit(g.screen, (0, 0))
        frame.blit(font.render([c for s, c in caps if t >= s][-1], True, (255, 255, 255)), (18, H + 12))
        ff.stdin.write(pygame.image.tobytes(frame, 'RGB')); t += dt
    ff.stdin.close(); ff.wait()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-vf', 'scale=1280:-2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '25',
                    '-movflags', '+faststart', BASE + '.mp4'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-t', '30', '-vf',
                    'fps=10,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4', BASE + '.gif'], check=True)
    os.remove(raw)


def signalready():
    src = '/tmp/SeptHackathon2026/demo/SignalReady_demo.mp4'
    subprocess.run(['cp', src, BASE + '.mp4'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf',
                    'setpts=PTS/6,fps=6,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=5', BASE + '.gif'], check=True)


# ---------------------------------------------------------------- dispatch
async def main():
    if NAME == 'ai-project-management-assistant':
        await wait_for_http('http://localhost:5173/login'); await record(BASE, ai_pm)
    elif NAME == 'emergency-response-platform':
        await wait_for_http('http://localhost:5174/login'); await record(BASE, emergency)
    elif NAME == 'enterprise-inventory-system':
        await wait_for_http('http://localhost:5173/login'); await wait_for_http('http://localhost:8080/swagger/index.html'); await record(BASE, inventory)
    elif NAME == 'supportflow-helpdesk':
        await supportflow()
    elif NAME == 'childcare-inventory':
        d = os.path.join(ROOT, 'projects/childcare-inventory-system')
        srv = bg('rm -f inventory.db && python3 -c "import app; app.init_db(); app.app.run(port=5055)"', cwd=d)
        await wait_for_http('http://localhost:5055/login'); await record(BASE, childcare); srv.terminate()
    elif NAME == 'application-tracker':
        srv = bg('PORT=3000 node $NODE_FLAGS server.mjs', cwd=os.path.join(ROOT, 'showcase/application-tracker'))
        await wait_for_http('http://127.0.0.1:3000/'); await record(BASE, tracker); srv.terminate()
    elif NAME == 'prestige-construction':
        srv = bg('python3 -m http.server 8077', cwd=os.path.join(ROOT, 'projects/prestige-construction-website'))
        await wait_for_http('http://localhost:8077/index.html'); await record(BASE, prestige); srv.terminate()
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', BASE + '.mp4', '-vf',
                        'fps=5,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=5', BASE + '.gif'], check=True)
    else:
        {'sentinelhash': sentinelhash, 'support-ticket-api': ticket_api, 'dependency-lens': dependency_lens, 'csc500': csc500,
         'csc500-shopping-cart': csc500_cart, 'signal-siege': signal_siege, 'signalready': signalready}[NAME]()

asyncio.run(main())

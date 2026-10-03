"""One-time portfolio reorganization, run by the Record project demos workflow.

Moves projects into clean folder names, removes committed dependency folders,
fixes two build/runtime bugs, adds demo sections to every README and rebuilds
the portfolio website. Safe to re-run: it skips work that is already done.
"""
import os, re, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
RAW = 'https://raw.githubusercontent.com/Matthew-Uhlar/Portfolio/main/demos/'
PAGES = 'https://matthew-uhlar.github.io/Portfolio/demos/'
GH = 'https://github.com/Matthew-Uhlar/'
FENCE = chr(96) * 3


def run(cmd):
    print('+', cmd, flush=True)
    subprocess.run(['bash', '-c', cmd], check=True)


def read(p):
    return open(p, encoding='utf-8').read()


def write(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)


def replace(p, old, new):
    s = read(p)
    if new in s:
        return
    if old not in s:
        raise SystemExit(f'{p}: expected text not found: {old[:60]!r}')
    write(p, s.replace(old, new))


# 1. Folder layout --------------------------------------------------------------
MOVES = [('Major Projects/AIProjectManagementAssistant', 'projects/ai-project-management-assistant'),
         ('Major Projects/CloudEmergencyResponsePlatform', 'projects/emergency-response-platform'),
         ('Major Projects/EnterpriseInventorySystem', 'projects/enterprise-inventory-system'),
         ('Major Projects/JavaHelpDeskPlatform', 'projects/supportflow-helpdesk'),
         ('Major Projects/RustFileIntegrityMonitor', 'projects/sentinelhash'),
         ('Major Projects/SignalSiegePythonGame', 'projects/signal-siege'),
         ('Major Projects/ChildcareInventorySystem', 'projects/childcare-inventory-system'),
         ('Major Projects/PrestigeConstructionCo - Basic Website', 'projects/prestige-construction-website'),
         ('Old', 'archive')]
for src, dst in MOVES:
    if os.path.isdir(src):
        if os.path.dirname(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
        run(f'git mv "{src}" "{dst}"')
JUNK = r'\( -name node_modules -o -name __MACOSX -o -name .vs -o -name .idea -o -name .tmp -o -name bower_components \)'
run(f'find archive -type d {JUNK} -prune -print0 | xargs -0 -r git rm -r -q --cached --ignore-unmatch')
run(f'find archive -type d {JUNK} -prune -exec rm -rf {{}} +')
run('git rm -q --cached --ignore-unmatch projects/childcare-inventory-system/inventory.db; rm -f projects/childcare-inventory-system/inventory.db')
write('.gitignore', 'node_modules/\ndist/\ntarget/\n.venv/\n__pycache__/\n*.pyc\n.DS_Store\n__MACOSX/\n.vs/\n.idea/\nprojects/**/*.db\n')

# 2. Fix: Enterprise Inventory frontend did not compile -------------------------
FE = 'projects/enterprise-inventory-system/frontend'
for page in ('Assets', 'Inventory', 'Requests'):
    p = f'{FE}/src/pages/{page}.tsx'
    s = read(p)
    write(p, s.replace('useEffect(load,[])', 'useEffect(()=>{load()},[])'))
write(f'{FE}/src/vite-env.d.ts', '/// <reference types="vite/client" />\n')
write(f'{FE}/index.html', '<!doctype html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n'
      '    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
      '    <title>StockPilot | Inventory &amp; Asset Management</title>\n  </head>\n  <body>\n'
      '    <div id="root"></div>\n    <script type="module" src="/src/main.tsx"></script>\n  </body>\n</html>\n')
run(f'npx --yes prettier@3 --log-level warn --write "{FE}/src/**/*.{{ts,tsx,css}}" "{FE}/tsconfig.json"')

# 3. Fix: SupportFlow leaked password hashes and failed to serialize tickets ----
J = 'projects/supportflow-helpdesk/src/main/java/com/matthewuhlar/supportflow'
IMP = 'import com.fasterxml.jackson.annotation.JsonIgnore;\nimport jakarta.persistence.*;'
for f, getter in (('model/UserAccount.java', '    public String getPasswordHash()'),
                  ('model/TicketComment.java', '    public Ticket getTicket()'),
                  ('model/TicketHistory.java', '    public Ticket getTicket()')):
    replace(f'{J}/{f}', getter, '    @JsonIgnore\n' + getter)
    replace(f'{J}/{f}', 'import jakarta.persistence.*;', IMP)
svc = f'{J}/service/TicketService.java'
replace(svc, 'import org.springframework.stereotype.Service;', 'import org.hibernate.Hibernate;\nimport org.springframework.stereotype.Service;')
replace(svc, """    public List<Ticket> getTickets(TicketStatus status, TicketPriority priority) {
        if (status != null) {
            return ticketRepository.findByStatusOrderByCreatedAtDesc(status);
        }

        if (priority != null) {
            return ticketRepository.findByPriorityOrderByCreatedAtDesc(priority);
        }

        return ticketRepository.findAll();
    }

    public Ticket getTicket(long id) {
        return ticketRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("The ticket could not be found."));
    }
""", """    @Transactional(readOnly = true)
    public List<Ticket> getTickets(TicketStatus status, TicketPriority priority) {
        List<Ticket> tickets;

        if (status != null) {
            tickets = ticketRepository.findByStatusOrderByCreatedAtDesc(status);
        } else if (priority != null) {
            tickets = ticketRepository.findByPriorityOrderByCreatedAtDesc(priority);
        } else {
            tickets = ticketRepository.findAll();
        }

        tickets.forEach(this::loadDetails);
        return tickets;
    }

    @Transactional(readOnly = true)
    public Ticket getTicket(long id) {
        Ticket ticket = ticketRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("The ticket could not be found."));
        loadDetails(ticket);
        return ticket;
    }

    // Responses are serialized after the transaction closes (open-in-view is off),
    // so load the comment and history collections while the session is still open.
    private void loadDetails(Ticket ticket) {
        Hibernate.initialize(ticket.getComments());
        Hibernate.initialize(ticket.getHistory());
    }
""")

# 4. Demo sections in every README ---------------------------------------------
DEMOS = [
    ('projects/ai-project-management-assistant', 'ai-project-management-assistant', 'Sign in, move work across the sprint board with drag and drop, add a backlog item, then have the AI assistant generate user stories, review risk and summarize the sprint.'),
    ('projects/emergency-response-platform', 'emergency-response-platform', 'A dispatcher creates an incident, assigns a response unit, posts a status update that SignalR broadcasts to every client and reviews unit status.'),
    ('projects/enterprise-inventory-system', 'enterprise-inventory-system', 'Dashboard metrics, live inventory search, adding a stock item as an admin, asset tracking and the purchase request approval workflow.'),
    ('projects/supportflow-helpdesk', 'supportflow-helpdesk', 'A real terminal session against the running API: an employee files a ticket and is blocked from changing its status, a technician escalates it (with audit history) and comments, then an admin filters tickets and checks the dashboard. Ends with the Swagger UI.'),
    ('projects/sentinelhash', 'sentinelhash', 'Baseline a web server directory, simulate an attacker (config changes, a dropped web shell, a deleted page) and watch SentinelHash catch every change and export a JSON report.'),
    ('projects/signal-siege', 'signal-siege', 'Gameplay recorded from the real game loop: waves of three enemy types, the upgrade screen between waves, particles and screen shake.'),
    ('projects/childcare-inventory-system', 'childcare-inventory', 'Role-based login, low-stock dashboard, search, adding an item that drops below its minimum and the supply request approval workflow.'),
    ('projects/prestige-construction-website', 'prestige-construction', 'The marketing site layout: video hero, services, project gallery and the quote request form.'),
    ('showcase/application-tracker', 'application-tracker', 'Adding applications, status totals, search, filtering and editing an application as it moves through the pipeline.'),
    ('showcase/support-ticket-api', 'support-ticket-api', 'Integration tests, then a real curl session: list, create, move through the status workflow, a rejected invalid transition (409), comments and the reports endpoint.'),
    ('showcase/dependency-lens', 'dependency-lens', 'Analyzing a small TypeScript app: a circular dependency, an unresolved import, strict mode failing a CI-style run and Mermaid export.'),
]
PRESTIGE = """# Prestige Construction Website

A responsive marketing website for Prestige Construction Colorado, a general contractor I have done web and IT work for since 2020. I customized a free HTML5 template with the company's branding, services, project gallery and a quote request form.

## Features

- Responsive layout that adapts from desktop to phone
- Full-screen video hero with a call to action
- Services, portfolio gallery and team sections
- Quote and contact forms backed by a PHP mail handler (quote.php and secure_email_code.php)

## Tech Used

HTML5, CSS3, JavaScript, jQuery and PHP for form handling on the hosting server.

## Run Locally

    python -m http.server 8000

Then open http://localhost:8000. The forms need a PHP host with mail configured to actually send messages.

## Credits

Layout based on a free template and images from Unsplash. See [CREDITS.txt](CREDITS.txt).
"""
write('projects/prestige-construction-website/README.md', PRESTIGE)
for folder, demo, desc in DEMOS:
    p = f'{folder}/README.md'
    s = read(p)
    if 'Watch the full demo video' in s:
        continue
    lines = s.split('\n')
    title = lines[0]
    name = title.lstrip('# ').strip()
    block = (f'{title}\n\n[![{name} demo]({RAW}{demo}-demo.gif)]({PAGES}{demo}-demo.mp4)\n\n'
             f'**[Watch the full demo video (MP4)]({PAGES}{demo}-demo.mp4)** | {desc}\n\n')
    write(p, block + '\n'.join(lines[1:]).lstrip('\n'))

# 5. Root README -----------------------------------------------------------------
def row(link, what, stack, demo):
    return f'| {link} | {what} | {stack} | [Video]({PAGES}{demo}-demo.mp4) |'

write('README.md', '\n'.join([
    '# Matthew Uhlar | Software Portfolio', '',
    '**[Live portfolio site with demo videos](https://matthew-uhlar.github.io/Portfolio/)** | [LinkedIn](https://www.linkedin.com/in/matthew-uhlar-ssm-92623617a) | [GitHub profile](https://github.com/Matthew-Uhlar)', '',
    'Software developer in Austin, TX (open to remote) with a BS in Computer Science and an MS in AI and Machine Learning in progress. I build full stack applications with C# and ASP.NET Core, Java and Spring Boot and React with TypeScript on PostgreSQL. Every project below has a recorded demo so you can see it working before you clone anything.', '',
    '## Featured projects', '',
    '| Project | What it is | Stack | Demo |', '| --- | --- | --- | --- |',
    row('[Project Pilot: AI Project Management Assistant](projects/ai-project-management-assistant/)', 'Agile planning tool with a Kanban board and an AI assistant that drafts stories, points, risks and sprint summaries', 'C#, ASP.NET Core 8, EF Core, React, TypeScript, PostgreSQL, Docker', 'ai-project-management-assistant'),
    row('[SupportFlow Help Desk API](projects/supportflow-helpdesk/)', 'Ticketing API with roles, status workflows, comments, audit history and reporting', 'Java 21, Spring Boot 3, Spring Security, JPA, PostgreSQL, JUnit 5', 'supportflow-helpdesk'),
    row('[Response Grid: Emergency Response Platform](projects/emergency-response-platform/)', 'Real-time dispatch app with live updates over SignalR', 'C#, ASP.NET Core 8, SignalR, React, PostgreSQL, Docker', 'emergency-response-platform'),
    row('[SignalReady](https://github.com/Matthew-Uhlar/signalready)', 'Predictive maintenance modeling studio (ABB Accelerator Hackathon 2026)', 'Python, scikit-learn, pandas, Streamlit', 'signalready'),
    row('[StockPilot: Enterprise Inventory System](projects/enterprise-inventory-system/)', 'Inventory, asset tracking and purchase request approvals', 'C#, ASP.NET Core 8, React, TypeScript, PostgreSQL, Docker', 'enterprise-inventory-system'),
    row('[SentinelHash](projects/sentinelhash/)', 'File integrity monitor that catches added, modified and deleted files', 'Rust, Rayon, Serde, Clap', 'sentinelhash'),
    '', '## More projects', '', '| Project | What it is | Stack | Demo |', '| --- | --- | --- | --- |',
    row('[Childcare Inventory System](projects/childcare-inventory-system/)', 'Supply tracking and request approvals for a childcare center', 'Python, Flask, SQLite', 'childcare-inventory'),
    row('[Signal Siege](projects/signal-siege/)', 'Wave survival game with all graphics drawn in code', 'Python, Pygame', 'signal-siege'),
    row('[Prestige Construction website](projects/prestige-construction-website/)', 'Marketing site for a Colorado general contractor', 'HTML, CSS, JavaScript, PHP', 'prestige-construction'),
    row('[Application Tracker](showcase/application-tracker/)', 'Job search pipeline with validated JSON backups', 'TypeScript, Node.js', 'application-tracker'),
    row('[Support Ticket API](showcase/support-ticket-api/)', 'Standard-library API with SQLite transactions and integration tests', 'Python, SQLite', 'support-ticket-api'),
    row('[Dependency Lens](showcase/dependency-lens/)', 'CLI that maps JS/TS imports and finds cycles', 'JavaScript, Node.js', 'dependency-lens'),
    row('[CSC500 Shopping Cart](https://github.com/Matthew-Uhlar/CSC500-Portfolio)', 'Object-oriented Python final project', 'Python', 'csc500-shopping-cart'),
    '', '## Repository layout', '', FENCE + 'text',
    'projects/   full applications, each with its own README, Docker setup where relevant and demo',
    'showcase/   smaller focused projects with tests run by GitHub Actions, plus the portfolio website',
    'demos/      recorded demo videos (MP4) and previews (GIF)',
    'archive/    earlier coursework and older projects, kept for reference', FENCE, '',
    'Demos are recorded by the [Record project demos](.github/workflows/record-demos.yml) workflow. It builds each app (Docker Compose for the full stack ones), drives it with a scripted Playwright browser or terminal session and commits the video, so every demo shows the code in this repository actually running.', '',
    '## About this work', '',
    'These are portfolio projects rather than claims of production deployments. I used AI assistance during development and review. The source, tests and documented limitations are here so the work can be evaluated directly.', '']))

# 6. Portfolio website -----------------------------------------------------------
FEAT = [
    ('ai-project-management-assistant', 'Project Pilot', 'AI project management assistant', 'Agile planning tool with JWT roles, sprints, a drag and drop Kanban board and an assistant that drafts user stories, suggests points, flags risks and summarizes sprints. The AI layer sits behind an interface so a hosted LLM can be swapped in.', 'C#|ASP.NET Core 8|EF Core|React|TypeScript|PostgreSQL|Docker', GH + 'ai-project-management-assistant'),
    ('supportflow-helpdesk', 'SupportFlow', 'Help desk API', 'Ticketing service with employee, technician and admin roles, enforced status workflows, comments, an audit trail of every change and reporting. Secured with Spring Security and JWT, documented with OpenAPI.', 'Java 21|Spring Boot 3|Spring Security|JPA|PostgreSQL|JUnit 5', GH + 'supportflow-helpdesk'),
    ('emergency-response-platform', 'Response Grid', 'Real-time emergency dispatch', 'Dispatchers create incidents, assign units and post updates that reach every connected client instantly over SignalR, with an incident timeline and map-ready coordinates.', 'C#|ASP.NET Core 8|SignalR|React|PostgreSQL|Docker', GH + 'emergency-response-platform'),
    ('signalready', 'SignalReady', 'Predictive maintenance ML studio', 'ABB Accelerator Hackathon 2026 solo build. Checks data readiness, catches label-leaking columns, compares models on held-out data and explains what the model relied on.', 'Python|scikit-learn|pandas|Streamlit|pytest', GH + 'signalready'),
    ('enterprise-inventory-system', 'StockPilot', 'Inventory and asset management', 'Inventory with reorder alerts, asset assignments and a purchase request approval workflow with role based permissions.', 'C#|ASP.NET Core 8|React|TypeScript|PostgreSQL', GH + 'enterprise-inventory-system'),
    ('sentinelhash', 'SentinelHash', 'File integrity monitor', 'Rust CLI that baselines a directory with parallel SHA-256 hashing and reports added, modified and deleted files as text or JSON.', 'Rust|Rayon|Serde|Clap', GH + 'sentinelhash'),
]
MORE = [
    ('childcare-inventory', 'Childcare Inventory System', 'Flask app for a childcare center: low-stock alerts and supply request approvals.', 'Python|Flask|SQLite', GH + 'Portfolio/tree/main/projects/childcare-inventory-system'),
    ('application-tracker', 'Application Tracker', 'Job search pipeline with validated data and JSON backups, no runtime dependencies.', 'TypeScript|Node.js', GH + 'Portfolio/tree/main/showcase/application-tracker'),
    ('support-ticket-api', 'Support Ticket API', 'Standard-library Python API with SQLite transactions and integration tests.', 'Python|SQLite', GH + 'Portfolio/tree/main/showcase/support-ticket-api'),
    ('dependency-lens', 'Dependency Lens', 'CLI that maps JS/TS imports and finds cycles with Tarjan&#39;s algorithm.', 'JavaScript|Node.js', GH + 'Portfolio/tree/main/showcase/dependency-lens'),
    ('signal-siege', 'Signal Siege', 'Wave survival game with all graphics drawn in code.', 'Python|Pygame', GH + 'Portfolio/tree/main/projects/signal-siege'),
    ('prestige-construction', 'Prestige Construction', 'Responsive marketing site for a Colorado general contractor.', 'HTML|CSS|JavaScript|PHP', GH + 'Portfolio/tree/main/projects/prestige-construction-website'),
]
def tags(t):
    return '<ul class="tags">' + ''.join(f'<li>{x}</li>' for x in t.split('|')) + '</ul>'
cards = ''.join(f"""
      <article class="card">
        <a class="thumb" href="demos/{d}-demo.mp4" aria-label="Watch the {n} demo video"><img src="demos/{d}-demo.gif" alt="Animated preview of {n}" loading="lazy" /><span class="play">Watch demo</span></a>
        <div class="body"><p class="kicker">{k}</p><h3>{n}</h3><p>{desc}</p>{tags(t)}
          <p class="links"><a href="demos/{d}-demo.mp4">Demo video</a><a href="{url}">Source code</a></p></div>
      </article>""" for d, n, k, desc, t, url in FEAT)
minis = ''.join(f"""
      <article class="mini">
        <a class="thumb" href="demos/{d}-demo.mp4" aria-label="Watch the {n} demo video"><img src="demos/{d}-demo.gif" alt="Animated preview of {n}" loading="lazy" /></a>
        <h3>{n}</h3><p>{desc}</p>{tags(t)}<p class="links"><a href="demos/{d}-demo.mp4">Demo</a><a href="{url}">Code</a></p>
      </article>""" for d, n, desc, t, url in MORE)
write('showcase/index.html', f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Matthew Uhlar, software developer in Austin, TX. Full stack .NET, Java and React projects with recorded demos." />
    <title>Matthew Uhlar | Software Developer</title>
    <link rel="stylesheet" href="portfolio.css?v=3" />
  </head>
  <body>
    <a class="skip" href="#projects">Skip to projects</a>
    <header class="wrap top">
      <a class="wordmark" href="https://github.com/Matthew-Uhlar">MU<span> / Matthew Uhlar</span></a>
      <nav><a href="#projects">Projects</a><a href="https://github.com/Matthew-Uhlar">GitHub</a><a href="https://www.linkedin.com/in/matthew-uhlar-ssm-92623617a">LinkedIn</a><a href="mailto:mattuhlar@gmail.com">Email</a></nav>
    </header>
    <main class="wrap">
      <section class="intro">
        <p class="eyebrow">SOFTWARE DEVELOPER / AUSTIN, TX / OPEN TO REMOTE</p>
        <h1>Full stack apps that<br /><span>solve real business problems.</span></h1>
        <p class="lead">I build with C# and ASP.NET Core, Java and Spring Boot and React with TypeScript on PostgreSQL. BS in Computer Science, MS in AI and Machine Learning in progress and a Certified SAFe Scrum Master with years of running IT and operations for growing organizations.</p>
        <p class="cta"><a class="button" href="#projects">See the demos</a><a class="button ghost" href="mailto:mattuhlar@gmail.com">Get in touch</a></p>
      </section>
      <section id="projects">
        <div class="section-heading"><h2>Featured projects</h2><span>Every project has a recorded demo</span></div>
        <div class="grid">{cards}
        </div>
      </section>
      <section>
        <div class="section-heading"><h2>More work</h2><span>Smaller tools, games and sites</span></div>
        <div class="grid small">{minis}
        </div>
      </section>
      <section class="about">
        <h2>How I work</h2>
        <p>I like projects with a concrete problem and a clear way to check the result. Each repository has setup instructions, sample data, tests where they matter and notes about what I would improve next. The demos are recorded automatically by a GitHub Actions workflow that builds and drives each app, so what you see is the code in the repository running. These are portfolio projects built with AI-assisted tooling, not claims of production deployments.</p>
      </section>
    </main>
    <footer class="wrap"><span>Matthew Uhlar &middot; Austin, TX</span><span><a href="mailto:mattuhlar@gmail.com">mattuhlar@gmail.com</a></span></footer>
  </body>
</html>
""")
write('showcase/portfolio.css', """:root{color-scheme:light;--paper:#f6f5ef;--ink:#192c29;--muted:#4c625c;--line:#cbd1c6;--accent:#315c47;--card:#fffefa}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.6}
a{color:inherit;text-underline-offset:4px}a:hover{color:var(--accent)}a:focus-visible{outline:3px solid #ae4d21;outline-offset:4px}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:16px;background:#fff;padding:8px}
.wrap{width:min(1180px,calc(100% - 32px));margin-inline:auto}
.top{padding-block:24px;display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line);font-size:14px;flex-wrap:wrap}
.top nav{display:flex;gap:18px;flex-wrap:wrap}.top nav a{text-decoration:none}
.wordmark{font-size:20px;font-weight:800;text-decoration:none}.wordmark span{font-size:14px;font-weight:500;margin-left:10px}
.intro{padding-block:64px 40px;max-width:860px}
.eyebrow{font-size:12px;letter-spacing:.14em;color:var(--muted);font-weight:700}
h1{font-size:clamp(34px,6vw,62px);line-height:1.05;margin:12px 0 20px;letter-spacing:-.02em}h1 span{color:var(--accent)}
.lead{font-size:18px;color:var(--muted);max-width:720px}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.button{display:inline-block;background:var(--ink);color:var(--paper);padding:12px 20px;border-radius:999px;text-decoration:none;font-weight:600}
.button:hover{background:var(--accent);color:#fff}.button.ghost{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.section-heading{display:flex;justify-content:space-between;align-items:baseline;gap:12px;border-top:1px solid var(--line);padding-top:28px;margin-top:24px;flex-wrap:wrap}
.section-heading h2{margin:0;font-size:28px}.section-heading span{color:var(--muted);font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px;margin-block:24px 48px}
.grid.small{grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
.card,.mini{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.thumb{position:relative;display:block;aspect-ratio:16/9;background:#10201d;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.play{position:absolute;right:12px;bottom:12px;background:rgba(25,44,41,.9);color:#fff;font-size:13px;font-weight:600;padding:6px 12px;border-radius:999px}
.body{padding:18px 20px 20px}.kicker{margin:0;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);font-weight:700}
.card h3{margin:4px 0 8px;font-size:22px}.mini h3{margin:14px 16px 4px;font-size:18px}
.card p,.mini p{margin:0 0 10px;color:var(--muted)}.mini p{margin-inline:16px;font-size:15px}
.tags{list-style:none;padding:0;margin:8px 0 12px;display:flex;flex-wrap:wrap;gap:6px}.mini .tags{margin-inline:16px}
.tags li{font-size:12px;border:1px solid var(--line);border-radius:999px;padding:2px 10px;background:var(--paper)}
.links{display:flex;gap:16px;font-weight:600}.links a{color:var(--accent)}.mini .links{margin:0 16px 16px}
.about{border-top:1px solid var(--line);padding-block:28px 48px;max-width:860px}.about h2{font-size:28px;margin:0 0 8px}.about p{color:var(--muted)}
footer{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding-block:24px;font-size:14px;color:var(--muted);flex-wrap:wrap}
@media (max-width:420px){.grid,.grid.small{grid-template-columns:1fr}}
""")
print('setup complete')

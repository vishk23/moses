## 2025-03-08
Yesterday, I built this orchestrator and was able to get celery-beat and workers running to handle tasks and requests asynchronously. Of course, I'm putting concurrency = 1 because I don't want processes to conflict, but it can handle async if needed.

Through periodic tasks, I'm able to schedule workflows to run. I just have a few sample workflows, but this should be easily transportable.

## 2025-03-09
Attemped adding logging, but not really working with waitress. 
    - circle back on this later on.

Waitress works and runs fine. I'll merge this into master branch because we could always swap back to runserver if needed. Waitress is supposed to be better than runserver, but let's look at pros and cons. This isn't a super sensitive.

Security level stuff, like getting users to sign in to track the on-demand requests is key.

I also need to learn how to configure the application to accept from different hosts. IT will do this, but it's good for me to understand.

I've been building this out and it seems to work well, thinking about how to transport.

Additionally, I don't have the core status page thing up and running yet. That isn't even high level, because I know how it runs. It'll be a master function that accepts args and then processes a script. I'm not sure why I'm avoiding it like the plague, just go the shed.

Learned a good bit about the Allowed Hosts and this is not what I thought it was.
- we limited access to site via OS firewall
- we limit the sites that they can access at via the allowed-hosts. This is in the header when they make the web request. Some sites can use the host header to generate download links and stuff based on host header. I'm not sure what django would rely on host header on out of the box, but it's good to be aware of. I'm limiting to 127.0.0.1 and localhost for now and I'll extend this to static IP address of VM once operational.

I still haven't configured any views for other users to use. That's the next key piece. I want to have this running where I have a static html form where the user can access via /status_page.

### Learning about internal access only on VPN or from specific IP addresses

To make your Django app accessible only to users within your company’s internal network (including those connected via VPN) on a Windows environment, you can bind it to an internal domain like `reportcontrolpanel.com` that is only resolvable within the network. Here’s a step-by-step guide to set this up securely:

---

### Step 1: Set Up Internal DNS for the Domain
Since you want your app to be accessible via an internal URL like `reportcontrolpanel.com`, you need to ensure this domain is only resolvable within your company network or for users connected via VPN.

- **What to do**:
  - Your company’s internal DNS server must have a record for `reportcontrolpanel.com` pointing to the internal IP address of the server hosting your Django app (e.g., `192.168.1.100`).
  - This domain should **not resolve** outside the network (e.g., from the public internet) or for users not connected via VPN.

- **How to proceed**:
  - If you have access to the DNS server, add an **A record** for `reportcontrolpanel.com` mapping to your server’s internal IP (e.g., `192.168.1.100`).
  - If you don’t manage the DNS, contact your IT department to set this up in the company’s internal DNS server.

- **Why this works**:
  - Users on the internal network or VPN will resolve `reportcontrolpanel.com` to your server’s IP, while external users won’t be able to find it, adding a layer of restriction.

---

### Step 2: Configure the Windows Firewall to Restrict Access
To ensure that only users from your company network (including VPN) can connect to your app, configure the server’s firewall to allow incoming connections only from specific IP ranges.

#### Steps to Set Up Windows Firewall:
1. **Open Windows Defender Firewall with Advanced Security**:
   - Press `Win + R`, type `wf.msc`, and press Enter.

2. **Create a New Inbound Rule**:
   - In the left pane, click **Inbound Rules**.
   - In the right pane, click **New Rule...**.

3. **Configure the Rule**:
   - **Rule Type**: Select **Port** and click **Next**.
   - **Protocol and Ports**: Choose **TCP**, then enter the port your app will use (e.g., `8000`). Click **Next**.
   - **Action**: Select **Allow the connection** and click **Next**.
   - **Profile**: Check all profiles (**Domain**, **Private**, **Public**) and click **Next**.

4. **Restrict to Internal and VPN IP Ranges**:
   - In the **Scope** section, under **Remote IP address**, select **These IP addresses**.
   - Click **Add...** and enter the IP ranges used by your company network and VPN.
     - Example: `192.168.0.0/16` (e.g., `192.168.0.0 - 192.168.255.255`) for internal network, `10.0.0.0/8` (e.g., `10.0.0.0 - 10.255.255.255`) for VPN.
     - Ask your IT team for the exact ranges if unsure.
   - Click **Next**.

5. **Name the Rule**:
   - Enter a name like "Django App - Internal and VPN Only" and click **Finish**.

- **Result**:
  - Only devices with IPs in the specified ranges can connect to your app’s port (e.g., `8000`). Even if someone outside the network knows your server’s IP, the firewall will block their connection.

---

### Step 3: Configure Django to Accept the Internal Domain
In your Django app, configure the `ALLOWED_HOSTS` setting to only accept requests for `reportcontrolpanel.com`. This ensures that even if someone from an allowed IP tries to access the app with a different `Host` header, Django will reject it.

- **Edit your Django `settings.py`**:
  ```python
  ALLOWED_HOSTS = ['reportcontrolpanel.com']
  ```

- **Why this is important**:
  - Django checks the `Host` header of every incoming request against `ALLOWED_HOSTS`. If it doesn’t match (e.g., someone tries `Host: fake.com`), the request is denied with a 400 Bad Request error.
  - This prevents internal users from misusing the app by spoofing the `Host` header.

---

### Step 4: Run the Django App with Waitress
Use Waitress (a production-ready WSGI server for Python) to serve your Django app, binding it to your server’s internal IP address.

- **Command to run Waitress**:
  ```bash
  waitress-serve --port=8000 --host=192.168.1.100 my_project.wsgi:application
  ```
  - Replace `192.168.1.100` with your server’s actual internal IP address (check with `ipconfig` in Command Prompt if unsure).
  - Replace `my_project.wsgi:application` with your Django project’s WSGI module (e.g., if your project is named `myapp`, it might be `myapp.wsgi:application`).

- **What this does**:
  - `--host=192.168.1.100`: Binds the app to the internal IP, so it only listens for connections on that address.
  - `--port=8000`: Specifies the port users will connect to (e.g., `http://reportcontrolpanel.com:8000`).

- **Alternative**:
  - If your server has multiple network interfaces and you’re confident in your firewall setup, you can bind to all interfaces:
    ```bash
    waitress-serve --port=8000 --host=0.0.0.0 my_project.wsgi:application
    ```
  - This listens on all interfaces, but the firewall (Step 2) ensures only internal/VPN users can connect. For extra security, binding to the specific IP (e.g., `192.168.1.100`) is preferred.

- **Install Waitress if needed**:
  - Run `pip install waitress` in your Python environment if it’s not already installed.

---

### How It All Fits Together
- **DNS**: `reportcontrolpanel.com` resolves to `192.168.1.100` only for users on the internal network or VPN.
- **Firewall**: Blocks all connections to port `8000` except from internal and VPN IP ranges.
- **Django**: Only accepts requests with `Host: reportcontrolpanel.com`.
- **Waitress**: Listens on the internal IP (or all interfaces with firewall protection), serving the app on port `8000`.

Users can access your app at `http://reportcontrolpanel.com:8000`, but only if they’re on the company network or connected via VPN.

---

### Testing Your Setup
1. **From an internal machine or VPN**:
   - Open a browser and go to `http://reportcontrolpanel.com:8000`.
   - It should work if everything is configured correctly.

2. **From outside the network (no VPN)**:
   - Try resolving `reportcontrolpanel.com` (e.g., `ping reportcontrolpanel.com` in Command Prompt).
   - It should fail to resolve, confirming external users can’t access it.

3. **Check firewall restriction**:
   - From an allowed IP, connect to `http://192.168.1.100:8000` directly.
   - It should work, but only because the IP is allowed. Django will still enforce the `Host` header.

---

### Additional Notes
- **Port 8000**: You’re using `8000` (common for development), which is fine for an internal app. If you want a cleaner URL (e.g., `http://reportcontrolpanel.com` without the port), you could use port `80`, but this requires running Waitress as an administrator (e.g., `--port=80`) or setting up a reverse proxy like Nginx. For simplicity, stick with `8000` unless instructed otherwise.
- **IT Coordination**: If you don’t control the DNS or network setup, work with your IT team to ensure the domain and IP ranges are correctly configured.


### Changing topics
Ok, back to the development, the health check is the next piece. Let's be specific about we want the health check. I'll need django site up, celery beat up and worker up. Those all need to be on startup. There is a heartbeat component to the celery beat/work

Merged in feature branches


## 2025-03-18
Implemented a new feature here for chaining tasks, using the same function as before, but ability to set a periodic task with multiple json arguments

{"module":"src.early_payoff_report","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"}
{"module":"src.daily_processing","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"}
{"module":"src.report_generator","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"}
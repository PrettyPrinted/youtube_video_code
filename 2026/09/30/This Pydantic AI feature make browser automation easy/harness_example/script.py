from pydantic_ai import Agent
from pydantic_ai_harness import FileSystem, SubAgent, SubAgents
from pydantic_ai_harness.browser_use import BrowserUse
from browser_use import BrowserProfile
from browser_use.browser.profile import ProxySettings

japan_proxy_config = ProxySettings(
    server='PROXY_SERVER',
    username='PROXY_USERNAME',
    password='PROXY_PASSWORD'
)

japan_profile = BrowserProfile(proxy=japan_proxy_config)

japan_agent = Agent('openai:gpt-6-luna',
    name='japan news researcher',
    description='A researcher focused on gathering news from Japan',
    capabilities=[BrowserUse(
        browser_profile=japan_profile,
        llm='openai:gpt-6-luna',
        allowed_domains=['msn.com'],
        headless=False,
        extend_system_message='You are to only use msn.com. Do not search or visit any other websites. You have the IP address of a user in Japan, so msn.com will be your primary source for news because it will be local to Japan'
    )]
)

austria_proxy_config = ProxySettings(
    server='PROXY_SERVER',
    username='PROXY_USERNAME',
    password='PROXY_PASSWORD'
)

austria_profile = BrowserProfile(proxy=austria_proxy_config)

austria_agent = Agent('openai:gpt-6-luna',
    name='Austria news researcher',
    description='A researcher focused on gathering news from Austria',
    capabilities=[BrowserUse(
        browser_profile=austria_profile,
        llm='openai:gpt-6-luna',
        allowed_domains=['msn.com'],
        headless=False,
        extend_system_message='You are to only use msn.com. Do not search or visit any other websites. You have the IP address of a user in Austria, so msn.com will be your primary source for news because it will be local to Austria'
    )]
)

agent = Agent('openai:gpt-6-luna',
    capabilities=[SubAgents(agents=[SubAgent(japan_agent), SubAgent(austria_agent)]), FileSystem(root_dir='./workspace')]
)

app = agent.to_web()
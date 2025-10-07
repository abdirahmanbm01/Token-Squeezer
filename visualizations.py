import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
from scipy.interpolate import make_interp_spline

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['mathtext.fontset'] = 'dejavuserif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12

sns.set_style("white")
sns.set_context("paper")

def create_modern_comprehensive_figure(result, analytics, batch_results, batch_analytics):
    """
    Combined Modern Scientific Visualization
    Split into two separate figures for better clarity
    """
    n_samples = len(batch_results)
    compression_ratios = np.array([r.savings_ratio * 100 for r in batch_results])
    avg_compression = np.mean(compression_ratios)
    
    fig1 = plt.figure(figsize=(18, 8))
    gs1 = fig1.add_gridspec(1, 2, hspace=0.3, wspace=0.3)
    
    ax_a = fig1.add_subplot(gs1[0, 0])
    
    all_ratios = compression_ratios
    
    kde = stats.gaussian_kde(all_ratios)
    x_range = np.linspace(all_ratios.min() - 5, all_ratios.max() + 5, 200)
    density = kde(x_range)
    
    for i in range(len(x_range)-1):
        color_val = (x_range[i] - x_range.min()) / (x_range.max() - x_range.min())
        color = plt.cm.plasma(color_val)
        ax_a.fill_between(x_range[i:i+2], 0, density[i:i+2], 
                        color=color, alpha=0.7, edgecolor='none')
    
    ax_a.plot(x_range, density, color='white', linewidth=3, alpha=0.8)
    
    ax_a.scatter(all_ratios, [0.002]*len(all_ratios), s=100, c='white', 
                edgecolors='black', linewidths=2, zorder=5, alpha=0.9,
                label=f'Observed samples (n={n_samples})')
    
    ax_a.axvline(x=avg_compression, color='#FFD700', linestyle='--', 
                linewidth=2.5, alpha=0.9, label=f'Mean: {avg_compression:.1f}%')
    
    ax_a.set_xlabel('Compression Ratio (%)', fontsize=14, fontweight='bold')
    ax_a.set_ylabel('Density', fontsize=14, fontweight='bold')
    ax_a.spines['top'].set_visible(False)
    ax_a.spines['right'].set_visible(False)
    ax_a.spines['left'].set_linewidth(2)
    ax_a.spines['bottom'].set_linewidth(2)
    ax_a.yaxis.grid(True, linestyle='--', alpha=0.2, linewidth=1)
    ax_a.set_axisbelow(True)
    ax_a.legend(loc='upper right', frameon=True, edgecolor='black',
              framealpha=0.95, fancybox=True, shadow=True, fontsize=11)
    ax_a.set_title(f'(a) Compression Ratio Distribution (n={n_samples} samples)', 
                  fontsize=15, loc='left', pad=15, fontweight='bold')
    
    stats_text = f'μ = {avg_compression:.1f}%\nσ = {np.std(compression_ratios):.1f}%\nRange: [{compression_ratios.min():.1f}%, {compression_ratios.max():.1f}%]'
    ax_a.text(0.02, 0.98, stats_text, transform=ax_a.transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black'))
    
    ax_b = fig1.add_subplot(gs1[0, 1])
    
    cumulative_savings = []
    running_total = 0
    for r in batch_results:
        cost_data = batch_analytics.calculate_cost_savings(r)
        running_total += cost_data['savings']
        cumulative_savings.append(running_total)
    
    x_range_savings = np.arange(1, len(cumulative_savings) + 1)
    
    if len(x_range_savings) > 3:
        x_smooth = np.linspace(x_range_savings.min(), x_range_savings.max(), 300)
        spl = make_interp_spline(x_range_savings, cumulative_savings, k=min(3, len(x_range_savings)-1))
        y_smooth = spl(x_smooth)
    else:
        x_smooth = x_range_savings
        y_smooth = cumulative_savings
    
    for i in range(len(x_smooth)-1):
        color_val = i / len(x_smooth)
        color = plt.cm.cool(color_val)
        ax_b.fill_between(x_smooth[i:i+2], 0, y_smooth[i:i+2],
                        color=color, alpha=0.5, edgecolor='none')
    
    ax_b.plot(x_smooth, y_smooth, color='#4C72B0', linewidth=3.5, alpha=0.9)
    
    ax_b.scatter(x_range_savings, cumulative_savings, s=120, c='white',
               edgecolors='#4C72B0', linewidths=3, zorder=3, alpha=0.9)
    
    final_savings = cumulative_savings[-1]
    ax_b.annotate(f'Total: ${final_savings:.4f}', 
                 xy=(x_range_savings[-1], final_savings),
                 xytext=(10, 10), textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                 fontsize=11, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2))
    
    if n_samples < 20:
        slope = final_savings / n_samples
        projection_x = np.array([n_samples, min(n_samples * 3, 50)])
        projection_y = slope * projection_x
        ax_b.plot(projection_x, projection_y, 'r--', linewidth=2, alpha=0.5,
                 label=f'Projection (${slope:.4f}/sample)')
        ax_b.legend(loc='upper left', frameon=True, edgecolor='black',
                   framealpha=0.95, fancybox=True, shadow=True, fontsize=10)
    
    ax_b.set_xlabel('Samples Processed', fontsize=14, fontweight='bold')
    ax_b.set_ylabel('Cumulative Cost Savings (USD)', fontsize=14, fontweight='bold')
    ax_b.spines['top'].set_visible(False)
    ax_b.spines['right'].set_visible(False)
    ax_b.spines['left'].set_linewidth(2)
    ax_b.spines['bottom'].set_linewidth(2)
    ax_b.grid(True, linestyle='--', alpha=0.2, linewidth=1)
    ax_b.set_axisbelow(True)
    ax_b.set_title('(b) Cumulative Cost Savings Across Samples', fontsize=15, loc='left',
                 pad=15, fontweight='bold')
    
    fig1.suptitle('Figure 1: Distribution and Economic Analysis\nPattern-Based Token Reduction for LLM Cost Optimization',
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    fig2 = plt.figure(figsize=(18, 8))
    gs2 = fig2.add_gridspec(1, 2, hspace=0.3, wspace=0.3)
    
    ax_c = fig2.add_subplot(gs2[0, 0])
    
    cost_data = analytics.calculate_cost_savings(result)
    costs = np.array([
        cost_data['original_cost'],
        cost_data['compressed_cost'],
        cost_data['savings']
    ])
    cost_labels = ['Original', 'Compressed', 'Savings']
    colors_cost = ['#4C72B0', '#55A868', '#C44E52']
    
    y_positions = [2, 1, 0]
    
    for i, (cost, label, color, y_pos) in enumerate(zip(costs, cost_labels, 
                                                         colors_cost, y_positions)):
        synthetic_data = np.random.normal(cost, cost * 0.02, 100)
        kde_cost = stats.gaussian_kde(synthetic_data)
        x_range_kde = np.linspace(synthetic_data.min(), synthetic_data.max(), 100)
        density = kde_cost(x_range_kde)
        density_normalized = density / density.max() * 0.35
        
        ax_c.fill_betweenx([y_pos - d for d in density_normalized], 
                         x_range_kde, cost, alpha=0.4, color=color)
        ax_c.plot(x_range_kde, [y_pos - d for d in density_normalized], 
                color=color, linewidth=2, alpha=0.8)
        
        ax_c.scatter([cost], [y_pos], s=200, c=color, edgecolors='white',
                   linewidths=2, zorder=3, alpha=0.9)
    
    ax_c.set_xlabel('Cost per Sample (USD)', fontsize=14, fontweight='bold')
    ax_c.set_ylabel('')
    ax_c.set_ylim(-0.8, 2.8)
    ax_c.set_yticks(y_positions)
    ax_c.set_yticklabels([f'{label}: ${cost:.5f}' for label, cost in zip(cost_labels, costs)],
                         fontsize=11, fontweight='bold')
    
    for tick_label, color in zip(ax_c.get_yticklabels(), colors_cost):
        tick_label.set_color(color)
    
    ax_c.spines['top'].set_visible(False)
    ax_c.spines['right'].set_visible(False)
    ax_c.spines['left'].set_linewidth(2)
    ax_c.spines['bottom'].set_linewidth(2)
    ax_c.xaxis.grid(True, linestyle='--', alpha=0.2, linewidth=1)
    ax_c.set_axisbelow(True)
    ax_c.set_title('(c) Cost Breakdown (single sample)', fontsize=15, loc='left', 
                 pad=15, fontweight='bold')
    
    legend_text = f'Compression: {result.savings_ratio*100:.1f}%\nCost Savings: {cost_data["savings_percentage"]:.1f}%'
    ax_c.text(0.98, 0.98, legend_text, transform=ax_c.transAxes,
             fontsize=10, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='black'))
    
    ax_d = fig2.add_subplot(gs2[0, 1])
    
    original_tokens = np.array([r.original_tokens for r in batch_results])
    compressed_tokens = np.array([r.compressed_tokens for r in batch_results])
    x = np.arange(len(batch_results))
    
    avg_reduction = np.mean((original_tokens - compressed_tokens) / original_tokens * 100)
    
    for i in range(len(x)-1):
        alpha = 0.3 + 0.6 * (i / len(x))
        ax_d.plot(x[i:i+2], original_tokens[i:i+2], 'o-', color='#4C72B0',
                linewidth=2.5, markersize=6, alpha=alpha, markeredgecolor='white',
                markeredgewidth=1.5)
    
    for i in range(len(x)-1):
        alpha = 0.3 + 0.6 * (i / len(x))
        ax_d.plot(x[i:i+2], compressed_tokens[i:i+2], 's-', color='#55A868',
                linewidth=2.5, markersize=6, alpha=alpha, markeredgecolor='white',
                markeredgewidth=1.5)
    
    ax_d.fill_between(x, original_tokens, compressed_tokens, alpha=0.25, 
                    color='#C44E52', label=f'Avg. reduction: {avg_reduction:.1f}%')
    
    ax_d.plot([], [], 'o-', color='#4C72B0', linewidth=2.5, markersize=8,
            label='Original Tokens', markeredgecolor='white', markeredgewidth=2)
    ax_d.plot([], [], 's-', color='#55A868', linewidth=2.5, markersize=8,
            label='Compressed Tokens', markeredgecolor='white', markeredgewidth=2)
    
    ax_d.set_xlabel('Sample Index', fontsize=14, fontweight='bold')
    ax_d.set_ylabel('Token Count', fontsize=14, fontweight='bold')
    
    n_ticks = min(20, len(batch_results))
    tick_indices = np.linspace(0, len(batch_results)-1, n_ticks, dtype=int)
    ax_d.set_xticks(tick_indices)
    ax_d.set_xticklabels([f'{i+1}' for i in tick_indices], fontsize=9, rotation=45)
    
    ax_d.spines['top'].set_visible(False)
    ax_d.spines['right'].set_visible(False)
    ax_d.spines['left'].set_linewidth(2)
    ax_d.spines['bottom'].set_linewidth(2)
    ax_d.yaxis.grid(True, linestyle='--', alpha=0.2, linewidth=1)
    ax_d.set_axisbelow(True)
    ax_d.legend(loc='upper right', frameon=True, edgecolor='black',
              framealpha=0.95, fancybox=True, shadow=True, fontsize=10)
    ax_d.set_title('(d) Token Count Reduction per Sample', 
                  fontsize=15, loc='left', pad=15, fontweight='bold')
    
    fig2.suptitle('Figure 2: Per-Sample Cost Analysis and Token Reduction Trajectory\nDetailed breakdown across sample corpus',
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    return fig1, fig2
sample_text = """
Please visit https://www.example-very-long-domain-name.com/api/v2/documentation/getting-started 
for the complete API documentation. You can also check out our GitHub repository at 
https://github.com/company-name/super-long-repository-name-for-demonstration.

To install the package, run:
```bash
npm install @company-namespace/very-long-package-name-that-saves-tokens
pip install super_long_python_package_name_for_demonstration_purposes
```

Contact us at support@company-with-very-long-domain-name.com or 
sales@another-example-domain-with-long-name.io for more information.

Here's a sample configuration in JSON format:
{"apiKey": "sk-proj-1234567890abcdef1234567890abcdef1234567890abcdef", 
 "endpoint": "https://api.example-service.com/v3/endpoints/processing", 
 "timeout": 30000, "retryAttempts": 5}

The file is located at /usr/local/lib/python3.9/site-packages/my_package_name/configuration/settings.py
or on Windows: C:\\Users\\Username\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\config.json

Version compatibility: requires someLibraryName >= 2.5.3 and anotherDependency == 1.8.7-beta.

Use the utility function `performComplexCalculationWithMultipleParameters` in your code.
"""

batch_texts = [
    "Check the docs at https://documentation.example-site.com/api/v2/reference and email help@support-center.com",
    "Run `pip install some-very-long-package-name` and `npm install @scope/another-long-package`",
    "The config file is at /home/user/projects/my-application/config/production/settings.json",
    "API key: sk-1234567890abcdef and endpoint: https://api.service-name.com/v1/process",
    """Use the following JSON: {"key": "value123456789", "url": "https://example.com/path/to/resource"}""",
    "Visit https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference for complete JavaScript documentation",
    "Contact support@enterprise-solutions-platform.com for enterprise inquiries and partnerships",
    "Install using `npm install --save-dev @testing-library/react-testing-utils`",
    "The configuration is in /opt/applications/production/config/database-settings.yaml",
    "Repository at https://github.com/open-source-foundation/machine-learning-toolkit",
    "Email notifications@automated-deployment-system.io for deployment updates",
    "Run `pip3 install tensorflow-gpu==2.12.0 numpy pandas scikit-learn`",
    "File path: C:\\Program Files\\Enterprise Software\\Configuration\\Production\\settings.json",
    "API endpoint: https://api.cloud-infrastructure-management.com/v3/resources",
    """Configuration: {"database": "postgresql://username:password@database-host.example.com:5432/dbname"}""",
    "Documentation at https://docs.python-web-framework.org/en/stable/tutorial/installation",
    "Support email: technical-assistance@software-development-company.com",
    "Install package: `npm install -g @command-line-interface/developer-tools`",
    "Located at /var/www/html/applications/production/static/configuration/app-settings.conf",
    "Clone from https://gitlab.enterprise-hosting.com/development-team/backend-services",
    "Notifications: automated-alerts@monitoring-and-observability-platform.com",
    "Command: `pip install --upgrade setuptools wheel build packaging-tools`",
    "Path: /home/developer/projects/web-application/frontend/src/components/navigation/settings.tsx",
    "Access at https://console.cloud-computing-platform.com/dashboard/analytics",
    """Settings: {"apiKey": "ak_live_1234567890abcdefghijklmnopqrstuvwxyz", "endpoint": "https://api.payment-processor.com/v2/transactions"}""",
    "Reference https://kubernetes.io/docs/concepts/workloads/controllers/deployment for deployment strategies",
    "Contact devops-engineering-team@infrastructure-automation-company.io",
    "Execute `docker run -d --name container-application -p 8080:80 application-image:latest`",
    "Config at /etc/systemd/system/application-service-manager.service.d/override.conf",
    "Repository https://bitbucket.org/software-engineering/microservices-architecture",
    "Alerts to incident-response-team@security-operations-center.com",
    "Install: `yarn add @user-interface-library/component-framework --dev`",
    "Location: C:\\Users\\Administrator\\AppData\\Roaming\\Application Data\\Configuration\\preferences.ini",
    "API https://rest-api-gateway.distributed-systems-platform.com/v4/endpoints",
    """Config: {"redisUrl": "redis://cache-cluster.example.com:6379/0", "mongoUrl": "mongodb://database-replica-set.example.com:27017/production"}""",
    "See https://react-native-documentation.org/docs/getting-started/installation-guide",
    "Support: customer-success-engineering@enterprise-saas-provider.com",
    "Run `cargo install --locked application-binary-package-manager`",
    "File: /usr/local/share/applications/production-environment/configuration/logging-settings.yaml",
    "GitHub https://github.com/artificial-intelligence/deep-learning-frameworks",
    "Email: automated-deployment-notifications@continuous-integration-platform.io",
    "Command `kubectl apply -f kubernetes-deployment-configuration.yaml --namespace production`",
    "Path /opt/containerized-applications/microservices/authentication-service/config/production.json",
    "Access https://admin-dashboard.content-management-system.com/settings/integrations",
    """Data: {"jwtSecret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "webhookUrl": "https://webhooks.integration-platform.com/events"}""",
    "Docs at https://spring-framework-documentation.io/spring-boot/reference/actuator",
    "Contact platform-engineering@distributed-computing-infrastructure.com",
    "Install `go install github.com/application-development-tools/code-generator@latest`",
    "Located /var/log/applications/production-environment/application-server-logs-archive/",
    "Clone https://gitlab.software-factory.org/devops/infrastructure-as-code-templates",
    "Notify operations-team@site-reliability-engineering-company.io",
    "Execute `mvn clean install -DskipTests=true -P production-profile`",
    "Config C:\\ProgramData\\Enterprise Applications\\Database Management\\connection-strings.config",
    "Endpoint https://graphql-api-gateway.serverless-architecture-platform.com/v1/query",
    """Settings: {"s3Bucket": "s3://production-data-storage-bucket-region-east/", "cloudFrontUrl": "https://cdn-distribution.cloudfront.net/"}""",
    "Guide at https://tensorflow-machine-learning.org/tutorials/quickstart/beginner",
    "Support machine-learning-operations@artificial-intelligence-platform.com",
    "Run `rustup update stable && cargo build --release --target x86_64-unknown-linux-gnu`",
    "Path /home/production/applications/web-services/backend-api/configuration/environment-variables.env",
    "Repository https://github.com/open-source-community/containerization-orchestration-tools",
    "Alerts infrastructure-monitoring@observability-and-alerting-platform.io",
    "Command `terraform apply -var-file=production.tfvars -auto-approve`",
    "File /etc/nginx/sites-available/application-reverse-proxy-configuration.conf",
    "Portal https://developer-console.cloud-native-platform.com/projects/applications",
    """Configuration: {"elasticsearchUrl": "https://elasticsearch-cluster.search-platform.com:9200", "kibanaUrl": "https://kibana-dashboard.visualization.com:5601"}""",
    "Documentation https://fastapi-modern-web-framework.tiangolo.com/tutorial/first-steps",
    "Contact backend-infrastructure-team@scalable-systems-engineering.com",
    "Install `pnpm add @frontend-framework/component-library @state-management/store`",
    "Located C:\\inetpub\\wwwroot\\production-applications\\web-services\\configuration\\appsettings.json",
    "API https://rest-api-orchestration-layer.microservices-platform.com/v5/services",
    """Config: {"kafkaBrokers": "kafka-broker-1.messaging-platform.com:9092,kafka-broker-2.messaging-platform.com:9092"}""",
    "Reference https://django-web-development-framework.readthedocs.io/en/stable/topics/auth",
    "Support full-stack-development@software-engineering-consultancy.io",
    "Execute `poetry install --no-dev --extras production && poetry run python manage.py migrate`",
    "Path /var/www/production-applications/frontend-react-application/build/static/configuration/",
    "Clone https://bitbucket.org/enterprise-development/continuous-deployment-pipelines",
    "Notify devops-automation-team@infrastructure-management-company.com",
    "Run `gradle clean build -Pprofile=production -x test --parallel`",
    "Config /opt/databases/postgresql/data/production/postgresql.conf.d/custom-settings.conf",
    "Dashboard https://monitoring-observability-platform.com/dashboards/infrastructure-metrics",
    """Settings: {"stripeKey": "sk_live_51234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij", "paypalClientId": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"}""",
    "Guide https://nextjs-react-framework.org/docs/advanced-features/custom-server-configuration",
    "Contact solutions-architecture@enterprise-technology-services.com",
    "Install `composer require symfony/symfony-framework-bundle vendor/application-package`",
    "File /usr/share/applications/production-environment/microservices/payment-processing/config.yaml",
    "Repository https://github.com/cloud-native-foundation/service-mesh-architecture-patterns",
    "Email platform-operations-center@distributed-systems-management.io",
    "Command `ansible-playbook -i production-inventory.yml deploy-application-playbook.yml --extra-vars`,",
    "Located C:\\Windows\\System32\\Configuration\\Enterprise Applications\\production-settings.xml",
    "Endpoint https://websocket-gateway.real-time-communication-platform.com/v2/connections",
    """Data: {"twilioAccountSid": "AC1234567890abcdef1234567890abcdef", "twilioAuthToken": "1234567890abcdef1234567890abcdef"}""",
    "Docs at https://vue-progressive-javascript-framework.vuejs.org/guide/essentials/application",
    "Support cloud-infrastructure-engineering@platform-as-a-service-provider.com",
    "Run `mix deps.get && mix ecto.migrate && mix phx.server --env production`",
    "Path /home/applications/production/elixir-phoenix-application/config/production.exs",
    "Clone https://gitlab.technology-company.com/platform-engineering/infrastructure-automation",
    "Notify incident-management@security-operations-and-response-team.io",
    "Execute `dotnet publish -c Release -r linux-x64 --self-contained -o ./publish/production`",
    "Config /etc/apache2/sites-enabled/production-application-virtual-host-configuration.conf",
    "Console https://administration-portal.enterprise-resource-planning-system.com/modules"
]

detector = PatternDetector(min_length=15)
compressor = CompressionEngine(detector)
analytics = TokenAnalytics()

print("="*80)
print("DEMO: SINGLE TEXT COMPRESSION")
print("="*80 + "\n")

result = compressor.compress(sample_text)
analytics.add_result(result)


restored, integrity, errors = RestorationEngine.restore(
    result.compressed_text, 
    result.placeholders
)


print("\n" + "="*80)
print("DEMO: BATCH PROCESSING")
print("="*80 + "\n")

compressor.reset_counter()
batch_analytics = TokenAnalytics()
batch_results = []

for idx, text in enumerate(batch_texts):
    result_batch = compressor.compress(text)
    batch_analytics.add_result(result_batch)
    batch_results.append(result_batch)
    if idx < 10 or idx % 10 == 0:  # Print first 10 and every 10th
        print(f"Text {idx + 1}: {result_batch.original_tokens} → {result_batch.compressed_tokens} "
              f"({result_batch.savings_ratio:.1%} saved)")

aggregate_stats = batch_analytics.get_aggregate_stats()
print(f"\nTotal compressions: {aggregate_stats['num_compressions']}")
print(f"Average compression ratio: {aggregate_stats['average_compression_ratio']:.1%}")
print(f"Total cost savings: ${aggregate_stats['total_cost_savings']:.4f}")

print("\n" + "="*80)
print("GENERATING MODERN COMPREHENSIVE FIGURE")
print("="*80 + "\n")

fig = create_modern_comprehensive_figure(result, analytics, batch_results, batch_analytics)
plt.show()

print("\n✓ All visualizations complete")
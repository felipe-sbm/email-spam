using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Email_Spam;
using Email_Spam.Services;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

var apiBase = builder.Configuration["ApiBaseUrl"];
var baseAddress = !string.IsNullOrEmpty(apiBase) ? new Uri(apiBase) : new Uri(builder.HostEnvironment.BaseAddress);
builder.Services.AddScoped(sp => new HttpClient { BaseAddress = baseAddress });
builder.Services.AddScoped<EmailService>(sp => new EmailService(sp.GetRequiredService<HttpClient>()));

await builder.Build().RunAsync();


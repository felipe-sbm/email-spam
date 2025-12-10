using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net.Http.Json;

namespace Email_Spam.Services
{
    public class EmailMessage
    {
        public int Id { get; set; }
        public string Sender { get; set; } = "";
        public string Recipient { get; set; } = "";
        public string Subject { get; set; } = "";
        public string Body { get; set; } = "";
        public DateTime Received { get; set; }
        public bool IsSpam { get; set; }
        public double SpamScore { get; set; }
    }

    public class EmailService
    {
        private List<EmailMessage> _emails = new();
        private readonly HttpClient _http;

        public event Action? OnEmailsChanged;
        public event Action? OnLoadingChanged;

        public bool IsLoading { get; private set; } = false;

        public EmailService(HttpClient http)
        {
            _http = http;
            // Iniciar carregamento assíncrono das mensagens do servidor
            _ = LoadFromServerAsync();
        }

        private class EmailDto
        {
            public int id { get; set; }
            public string sender { get; set; } = "";
            public string recipient { get; set; } = "";
            public string subject { get; set; } = "";
            public string body { get; set; } = "";
            public string received { get; set; } = "";
            public bool is_spam { get; set; }
            public double spam_score { get; set; }
        }

        private async Task LoadFromServerAsync()
        {
            IsLoading = true;
            OnLoadingChanged?.Invoke();
            try
            {
                var records = await _http.GetFromJsonAsync<List<EmailDto>>("/emails");
                if (records != null)
                {
                    _emails = records.Select(r => new EmailMessage
                    {
                        Id = r.id,
                        Sender = r.sender,
                        Recipient = r.recipient,
                        Subject = r.subject,
                        Body = r.body,
                        Received = string.IsNullOrEmpty(r.received) ? DateTime.MinValue : DateTime.Parse(r.received),
                        IsSpam = r.is_spam,
                        SpamScore = r.spam_score
                    }).OrderByDescending(e => e.Received).ToList();

                    OnEmailsChanged?.Invoke();
                }
            }
            catch
            {
                // Silencioso; UI continuará funcionando com lista vazia
            }
            finally
            {
                IsLoading = false;
                OnLoadingChanged?.Invoke();
            }
        }

        public List<EmailMessage> GetEmails()
        {
            return _emails.OrderByDescending(e => e.Received).ToList();
        }

        public List<EmailMessage> GetInboxEmails()
        {
            return _emails.Where(e => !e.IsSpam).OrderByDescending(e => e.Received).ToList();
        }

        public List<EmailMessage> GetSentEmails()
        {
            return _emails.Where(e => e.Sender == "me@example.com").OrderByDescending(e => e.Received).ToList();
        }

        public List<EmailMessage> GetSpamEmails()
        {
            return _emails.Where(e => e.IsSpam).OrderByDescending(e => e.Received).ToList();
        }

        public async Task<EmailMessage?> CreateEmailAsync(EmailMessage email)
        {
            try
            {
                var payload = new
                {
                    sender = email.Sender,
                    recipient = email.Recipient,
                    subject = email.Subject,
                    body = email.Body,
                    received = email.Received.ToString("o"),
                    is_spam = email.IsSpam,
                    spam_score = email.SpamScore
                };

                var resp = await _http.PostAsJsonAsync("/emails", payload);
                if (resp.IsSuccessStatusCode)
                {
                    var created = await resp.Content.ReadFromJsonAsync<EmailDto>();
                    if (created != null)
                    {
                        var msg = new EmailMessage
                        {
                            Id = created.id,
                            Sender = created.sender,
                            Recipient = created.recipient,
                            Subject = created.subject,
                            Body = created.body,
                            Received = string.IsNullOrEmpty(created.received) ? DateTime.MinValue : DateTime.Parse(created.received),
                            IsSpam = created.is_spam,
                            SpamScore = created.spam_score
                        };
                        _emails.Add(msg);
                        OnEmailsChanged?.Invoke();
                        return msg;
                    }
                }
            }
            catch
            {
                // ignore
            }

            return null;
        }

        public async Task ReloadAsync()
        {
            await LoadFromServerAsync();
        }

        public void DeleteEmail(EmailMessage email)
        {
            _emails.Remove(email);
            OnEmailsChanged?.Invoke();
        }

        public int GetSpamCount()
        {
            return _emails.Count(e => e.IsSpam);
        }

        public int GetInboxCount()
        {
            return _emails.Count(e => !e.IsSpam);
        }
    }
}

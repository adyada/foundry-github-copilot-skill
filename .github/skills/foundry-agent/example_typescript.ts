/**
 * Microsoft Foundry Agent Integration Example (TypeScript)
 * 
 * This example demonstrates a simplified REST API approach for calling
 * Microsoft Foundry agent applications with proper authentication.
 * 
 * Note: This is a conceptual example showing REST API patterns.
 * For production use with TypeScript, consider using the Azure SDK for JavaScript.
 * 
 * Prerequisites:
 *     npm install @azure/identity
 * 
 * Environment Variables:
 *     AZURE_AI_PROJECT_ENDPOINT: Your Foundry project endpoint
 *     AZURE_AGENT_ID: Your agent ID
 */

import { DefaultAzureCredential } from '@azure/identity';

/**
 * Configuration interface for Foundry agent client
 */
interface FoundryConfig {
    endpoint: string;
    agentId: string;
}

/**
 * Message structure for agent communication
 */
interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
}

/**
 * Agent request structure
 */
interface AgentRequest {
    messages: Message[];
    conversationId?: string;
    stream?: boolean;
}

/**
 * Agent response structure
 */
interface AgentResponse {
    messages: Message[];
    conversationId?: string;
    usage?: {
        promptTokens: number;
        completionTokens: number;
        totalTokens: number;
    };
}

/**
 * Client for interacting with Microsoft Foundry agents
 */
class FoundryAgentClient {
    private endpoint: string;
    private agentId: string;
    private credential: DefaultAzureCredential;
    private accessToken: string | null = null;
    private tokenExpiry: Date | null = null;

    constructor(config?: Partial<FoundryConfig>) {
        this.endpoint = config?.endpoint || process.env.AZURE_AI_PROJECT_ENDPOINT || '';
        this.agentId = config?.agentId || process.env.AZURE_AGENT_ID || '';
        
        if (!this.endpoint) {
            throw new Error('AZURE_AI_PROJECT_ENDPOINT must be set');
        }
        if (!this.agentId) {
            throw new Error('AZURE_AGENT_ID must be set');
        }
        
        this.credential = new DefaultAzureCredential();
        console.log(`✓ Initialized Foundry client for: ${this.endpoint}`);
    }

    /**
     * Get or refresh the access token
     */
    private async getAccessToken(): Promise<string> {
        const now = new Date();
        
        // Return cached token if still valid
        if (this.accessToken && this.tokenExpiry && this.tokenExpiry > now) {
            return this.accessToken;
        }
        
        try {
            // Request new token
            const tokenResponse = await this.credential.getToken(
                'https://cognitiveservices.azure.com/.default'
            );
            
            if (!tokenResponse) {
                throw new Error('Failed to acquire access token');
            }
            
            this.accessToken = tokenResponse.token;
            this.tokenExpiry = new Date(tokenResponse.expiresOnTimestamp);
            
            return this.accessToken;
        } catch (error) {
            console.error('✗ Failed to acquire token:', error);
            throw error;
        }
    }

    /**
     * Send a message to the Foundry agent
     */
    async sendMessage(
        message: string,
        conversationId?: string
    ): Promise<AgentResponse> {
        try {
            const token = await this.getAccessToken();
            
            const request: AgentRequest = {
                messages: [
                    {
                        role: 'user',
                        content: message
                    }
                ]
            };
            
            if (conversationId) {
                request.conversationId = conversationId;
            }
            
            console.log(`\n→ Sending message: ${message}`);
            
            // Note: This URL pattern is conceptual. Actual Foundry REST API
            // endpoints may differ. Refer to Azure AI Foundry documentation.
            const url = `${this.endpoint}/agents/${this.agentId}/invoke`;
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request)
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Agent call failed: ${response.status} ${response.statusText}\n${errorText}`);
            }
            
            const result: AgentResponse = await response.json();
            console.log('✓ Received response');
            
            return result;
            
        } catch (error) {
            console.error('✗ Error calling agent:', error);
            throw error;
        }
    }

    /**
     * Send a message with streaming response
     */
    async *sendMessageStream(
        message: string,
        conversationId?: string
    ): AsyncGenerator<string, void, unknown> {
        try {
            const token = await this.getAccessToken();
            
            const request: AgentRequest = {
                messages: [
                    {
                        role: 'user',
                        content: message
                    }
                ],
                stream: true
            };
            
            if (conversationId) {
                request.conversationId = conversationId;
            }
            
            console.log(`\n→ Sending message (streaming): ${message}`);
            
            // Note: This URL pattern is conceptual. Actual Foundry REST API
            // endpoints may differ. Refer to Azure AI Foundry documentation.
            const url = `${this.endpoint}/agents/${this.agentId}/invoke`;
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request)
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Agent call failed: ${response.status} ${response.statusText}\n${errorText}`);
            }
            
            if (!response.body) {
                throw new Error('Response body is null');
            }
            
            console.log('✓ Streaming response:');
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const { done, value } = await reader.read();
                
                if (done) {
                    break;
                }
                
                const chunk = decoder.decode(value, { stream: true });
                
                // Parse SSE format
                const lines = chunk.split('\n');
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.substring(6);
                        if (data === '[DONE]') {
                            return;
                        }
                        try {
                            const parsed = JSON.parse(data);
                            if (parsed.delta?.content) {
                                yield parsed.delta.content;
                            }
                        } catch {
                            // Skip invalid JSON
                        }
                    }
                }
            }
            
        } catch (error) {
            console.error('✗ Error calling agent:', error);
            throw error;
        }
    }
}

/**
 * Example 1: Simple agent call
 */
async function exampleSimpleCall(): Promise<boolean> {
    console.log('\n' + '='.repeat(60));
    console.log('Example 1: Simple Agent Call');
    console.log('='.repeat(60));
    
    try {
        // Initialize the client
        const client = new FoundryAgentClient();
        
        // Send a message
        const response = await client.sendMessage(
            'What is Microsoft Foundry and how does it help developers?'
        );
        
        // Process the response
        if (response.messages) {
            for (const msg of response.messages) {
                if (msg.role === 'assistant') {
                    console.log(`\nAgent Response:\n${msg.content}`);
                }
            }
        }
        
        console.log('\n✓ Example completed successfully');
        return true;
        
    } catch (error) {
        console.error('\n✗ Example failed:', error);
        return false;
    }
}

/**
 * Example 2: Streaming agent call
 */
async function exampleStreamingCall(): Promise<boolean> {
    console.log('\n' + '='.repeat(60));
    console.log('Example 2: Streaming Agent Call');
    console.log('='.repeat(60));
    
    try {
        // Initialize the client
        const client = new FoundryAgentClient();
        
        // Send a message with streaming
        console.log('\nAgent Response (streaming):');
        
        for await (const chunk of client.sendMessageStream(
            'Explain the benefits of using AI agents in software development.'
        )) {
            process.stdout.write(chunk);
        }
        
        console.log('\n\n✓ Example completed successfully');
        return true;
        
    } catch (error) {
        console.error('\n✗ Example failed:', error);
        return false;
    }
}

/**
 * Example 3: Multi-turn conversation
 */
async function exampleConversation(): Promise<boolean> {
    console.log('\n' + '='.repeat(60));
    console.log('Example 3: Multi-Turn Conversation');
    console.log('='.repeat(60));
    
    try {
        // Initialize the client
        const client = new FoundryAgentClient();
        
        // First message
        const response1 = await client.sendMessage(
            "I'm building a web application. What technology stack would you recommend?"
        );
        
        const conversationId = response1.conversationId;
        
        if (response1.messages) {
            for (const msg of response1.messages) {
                if (msg.role === 'assistant') {
                    console.log(`\nAgent Response 1:\n${msg.content}`);
                }
            }
        }
        
        // Follow-up message with conversation context
        if (conversationId) {
            const response2 = await client.sendMessage(
                'What about for a mobile app instead?',
                conversationId
            );
            
            if (response2.messages) {
                for (const msg of response2.messages) {
                    if (msg.role === 'assistant') {
                        console.log(`\nAgent Response 2:\n${msg.content}`);
                    }
                }
            }
        }
        
        console.log('\n✓ Example completed successfully');
        return true;
        
    } catch (error) {
        console.error('\n✗ Example failed:', error);
        return false;
    }
}

/**
 * Main function to run all examples
 */
async function main(): Promise<void> {
    console.log('Microsoft Foundry Agent Integration Examples');
    console.log('='.repeat(60));
    
    // Check environment variables
    const requiredVars = ['AZURE_AI_PROJECT_ENDPOINT', 'AZURE_AGENT_ID'];
    const missingVars = requiredVars.filter(varName => !process.env[varName]);
    
    if (missingVars.length > 0) {
        console.error(`\n✗ Error: Missing required environment variables: ${missingVars.join(', ')}`);
        console.error('\nPlease set the following environment variables:');
        console.error('  AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com');
        console.error('  AZURE_AGENT_ID=your-agent-id');
        process.exit(1);
    }
    
    // Run examples
    const examples = [
        exampleSimpleCall,
        exampleStreamingCall,
        exampleConversation
    ];
    
    const results: boolean[] = [];
    
    for (const example of examples) {
        try {
            const success = await example();
            results.push(success);
        } catch (error) {
            console.error('\n✗ Unexpected error:', error);
            results.push(false);
        }
    }
    
    // Summary
    console.log('\n' + '='.repeat(60));
    console.log('Summary');
    console.log('='.repeat(60));
    const successful = results.filter(r => r).length;
    const total = results.length;
    console.log(`Completed ${successful}/${total} examples successfully`);
    
    if (successful === total) {
        console.log('✓ All examples passed!');
        process.exit(0);
    } else {
        console.log('✗ Some examples failed');
        process.exit(1);
    }
}

// Run the examples if this file is executed directly
if (require.main === module) {
    main().catch(error => {
        console.error('Fatal error:', error);
        process.exit(1);
    });
}

export { FoundryAgentClient, FoundryConfig, Message, AgentRequest, AgentResponse };

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/app/components/ui/dialog';
import { Slider } from '@/app/components/ui/slider';
import { Label } from '@/app/components/ui/label';
import { Button } from '@/app/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/app/components/ui/tabs';
import { ScrollArea } from '@/app/components/ui/scroll-area';
import { Settings, Volume2, Activity, History, MessageSquare, User } from 'lucide-react';
import { toast } from 'sonner';

interface SettingsModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
}

interface HistoryItem {
    id: number;
    user_input: string;
    assistant_response: string;
    timestamp: string;
}

export function SettingsModal({ open, onOpenChange }: SettingsModalProps) {
    const [rate, setRate] = useState([150]);
    const [volume, setVolume] = useState([0.9]);
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [activeTab, setActiveTab] = useState("general");

    // Fetch config on open
    useEffect(() => {
        if (open) {
            fetchConfig();
            if (activeTab === 'history') fetchHistory();
        }
    }, [open, activeTab]);

    const fetchConfig = async () => {
        try {
            const res = await fetch('http://localhost:8000/api/config');
            const data = await res.json();

            if (data.tts) {
                setRate([data.tts.rate || 150]);
                setVolume([data.tts.volume || 0.9]);
            }
        } catch (error) {
            console.error("Failed to load config", error);
            toast.error("Failed to load settings");
        }
    };

    const fetchHistory = async () => {
        try {
            const res = await fetch('http://localhost:8000/api/history?limit=20');
            const data = await res.json();
            setHistory(data);
        } catch (error) {
            console.error("Failed to load history", error);
            toast.error("Failed to load history");
        }
    };

    const saveConfig = async () => {
        try {
            setLoading(true);
            const payload = {
                tts: {
                    rate: rate[0],
                    volume: volume[0]
                }
            };

            const res = await fetch('http://localhost:8000/api/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                toast.success("Settings saved successfully");
                onOpenChange(false);
            } else {
                throw new Error("Failed to save");
            }
        } catch (error) {
            console.error("Failed to save config", error);
            toast.error("Failed to save settings");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[500px] bg-zinc-950 border-zinc-800 text-zinc-100 max-h-[80vh] flex flex-col">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2 text-xl">
                        <Settings className="w-5 h-5 text-[var(--accent-primary)]" />
                        Settings
                    </DialogTitle>
                </DialogHeader>

                <Tabs defaultValue="general" value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col min-h-0">
                    <TabsList className="grid w-full grid-cols-2 bg-zinc-900">
                        <TabsTrigger value="general">General</TabsTrigger>
                        <TabsTrigger value="history">History</TabsTrigger>
                    </TabsList>

                    <TabsContent value="general" className="space-y-6 py-4">
                        {/* Speech Rate */}
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <Label className="text-zinc-400 flex items-center gap-2">
                                    <Activity className="w-4 h-4" /> Speech Rate
                                </Label>
                                <span className="text-sm font-mono text-zinc-500">{rate[0]} wpm</span>
                            </div>
                            <Slider
                                value={rate}
                                onValueChange={setRate}
                                min={50}
                                max={300}
                                step={10}
                                className="[&_.range-thumb]:bg-[var(--accent-primary)]"
                            />
                        </div>

                        {/* Volume */}
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <Label className="text-zinc-400 flex items-center gap-2">
                                    <Volume2 className="w-4 h-4" /> TTS Volume
                                </Label>
                                <span className="text-sm font-mono text-zinc-500">{Math.round(volume[0] * 100)}%</span>
                            </div>
                            <Slider
                                value={volume}
                                onValueChange={setVolume}
                                min={0}
                                max={1}
                                step={0.1}
                            />
                        </div>

                        <div className="flex justify-end gap-3 mt-8">
                            <Button variant="outline" onClick={() => onOpenChange(false)} className="border-zinc-800 hover:bg-zinc-900 text-zinc-300">
                                Cancel
                            </Button>
                            <Button onClick={saveConfig} disabled={loading} className="bg-[var(--accent-primary)] text-black hover:bg-[var(--accent-primary)]/90">
                                {loading ? 'Saving...' : 'Save Changes'}
                            </Button>
                        </div>
                    </TabsContent>

                    <TabsContent value="history" className="flex-1 min-h-0 flex flex-col py-4">
                        <ScrollArea className="flex-1 pr-4 -mr-4 h-[300px]">
                            <div className="space-y-4">
                                {history.length === 0 ? (
                                    <div className="text-center text-zinc-500 py-8">
                                        No history available
                                    </div>
                                ) : (
                                    history.map((item) => (
                                        <div key={item.id} className="bg-zinc-900/50 rounded-lg p-3 space-y-2 border border-white/5">
                                            <div className="flex items-start gap-2">
                                                <User className="w-4 h-4 text-zinc-400 mt-1 shrink-0" />
                                                <p className="text-sm text-zinc-300">{item.user_input}</p>
                                            </div>
                                            <div className="flex items-start gap-2 pl-2 border-l-2 border-[var(--accent-primary)]/30 ml-1">
                                                <MessageSquare className="w-4 h-4 text-[var(--accent-primary)] mt-1 shrink-0" />
                                                <p className="text-sm text-zinc-400">{item.assistant_response}</p>
                                            </div>
                                            <div className="text-[10px] text-zinc-600 text-right pt-1">
                                                {new Date(item.timestamp).toLocaleString()}
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </ScrollArea>
                    </TabsContent>
                </Tabs>
            </DialogContent>
        </Dialog>
    );
}

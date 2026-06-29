
from __future__ import annotations

from core import DashboardSection, ReleaseStatus, Settings


class ReleaseDashboardService:
    """Build v1.0 Release dashboard content.

    Sprint 1 is focused on the product shell:
    - one app entry
    - clear release status
    - dashboard sections
    - stable structure for future sprints
    """

    def __init__(self, settings: Settings):
        self.settings = settings

    def status(self) -> ReleaseStatus:
        return ReleaseStatus(
            name=self.settings.app_name,
            version=self.settings.version,
            channel=self.settings.release_channel,
            status="Release Sprint 1 active",
            next_focus="Future Leaders Ranking Engine v1",
        )

    def sections(self) -> list[DashboardSection]:
        return [
            DashboardSection(
                title="Market Snapshot",
                subtitle="Daily market context",
                status="Framework ready",
                items=[
                    "AI Infrastructure",
                    "Semiconductors",
                    "Cloud",
                    "Space / Defense",
                    "Healthcare AI",
                ],
            ),
            DashboardSection(
                title="Portfolio Snapshot",
                subtitle="STS portfolio intelligence",
                status="RC1 engine ready",
                items=[
                    "Strong winners",
                    "Under-pressure holdings",
                    "Near-cost positions",
                    "Deep-break alerts",
                ],
            ),
            DashboardSection(
                title="Future Leaders",
                subtitle="Discovery intelligence",
                status="Ranking engine next",
                items=[
                    "Top candidates",
                    "Research Cards",
                    "Winner DNA",
                    "Why selected",
                ],
            ),
            DashboardSection(
                title="Action Plan",
                subtitle="Next-step decision layer",
                status="RC1 engine ready",
                items=[
                    "Research",
                    "Watch",
                    "Hold / Trim",
                    "Review thesis",
                ],
            ),
            DashboardSection(
                title="Decision Coach",
                subtitle="Personalized decision memory",
                status="RC1 engine ready",
                items=[
                    "Avoid chasing",
                    "Avoid blind averaging down",
                    "Do not sell compounders too early",
                    "Plan before trimming winners",
                ],
            ),
        ]

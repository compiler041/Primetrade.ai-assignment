import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Button,
  IconButton,
  Avatar,
  Chip,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import LogoutIcon from "@mui/icons-material/Logout";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function TopNavigation({
  isSmallScreen,
  toggleDrawer,
}: {
  isSmallScreen: boolean;
  toggleDrawer: () => void;
}) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const displayName = user?.first_name
    ? `${user.first_name} ${user.last_name || ""}`.trim()
    : user?.email || "User";

  const initials = user?.first_name
    ? `${user.first_name[0]}${user.last_name?.[0] || ""}`.toUpperCase()
    : user?.email?.[0]?.toUpperCase() || "U";

  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
        background: "linear-gradient(135deg, #1a237e 0%, #3f51b5 100%)",
        boxShadow: "0 2px 20px rgba(63,81,181,0.4)",
      }}
    >
      <Toolbar>
        {isSmallScreen && (
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={toggleDrawer}
          >
            <MenuIcon />
          </IconButton>
        )}
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, fontWeight: 700, letterSpacing: 0.5 }}
        >
          🚀 Primetrade.ai Task Manager
        </Typography>

        {user && (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
            {user.is_superuser && (
              <Chip
                icon={<AdminPanelSettingsIcon sx={{ fontSize: 16 }} />}
                label="Admin"
                size="small"
                sx={{
                  bgcolor: "rgba(255,193,7,0.2)",
                  color: "#ffc107",
                  borderColor: "#ffc107",
                  fontWeight: 600,
                  border: "1px solid",
                  "& .MuiChip-icon": { color: "#ffc107" },
                }}
              />
            )}
            <Avatar
              sx={{
                width: 34,
                height: 34,
                bgcolor: "rgba(255,255,255,0.2)",
                fontSize: "0.85rem",
                fontWeight: 700,
              }}
            >
              {initials}
            </Avatar>
            <Typography
              variant="body2"
              sx={{ color: "rgba(255,255,255,0.9)", fontWeight: 500 }}
            >
              {displayName}
            </Typography>
            <IconButton
              color="inherit"
              onClick={handleLogout}
              size="small"
              title="Logout"
              sx={{
                bgcolor: "rgba(255,255,255,0.1)",
                "&:hover": { bgcolor: "rgba(255,255,255,0.2)" },
              }}
            >
              <LogoutIcon fontSize="small" />
            </IconButton>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
}
